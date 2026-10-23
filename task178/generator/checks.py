"""task178 checks: the assertions the build must pass before anyone reads the pack. Run as
    python3 task178/generator/checks.py task178/target
Every label is printed; the run fails on the first false one at the end with the count."""
from __future__ import annotations

import csv
import datetime as dt
import io
import json
import math
import os
import re
import shutil
import sys
import tempfile
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc  # noqa: E402
import common as C  # noqa: E402
import docs as D  # noqa: E402
import world as W  # noqa: E402

RESULTS = []


def ok(label, cond, detail=""):
    RESULTS.append((label, bool(cond), detail))
    print(("PASS " if cond else "FAIL ") + label + ((": " + str(detail)) if detail else ""))


def pdf_text(path):
    from pypdf import PdfReader
    return "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)


def norm_ws(s):
    return re.sub(r"\s+", " ", s)


def main(target):
    task = os.path.dirname(os.path.abspath(target))
    figs = json.load(open(os.path.join(task, "generator", "figures.json")))
    res = calc.call(target)
    g = res["golden"]
    setting = res["setting"]

    # ------------------------------------------------------------------ the input gates
    files = sorted(os.listdir(target))
    ok("gate: 10 or more files", len(files) >= 10, len(files))
    ok("gate: 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3, sorted({f.rsplit(".", 1)[1] for f in files}))
    ok("gate: every file the generator names ships", set(files) == set(C.ALL_FILES), set(files) ^ set(C.ALL_FILES))
    with open(os.path.join(target, C.F_FLOWS)) as fh:
        nflow = sum(1 for _ in fh) - 1
    ok("gate: a file of 25,000 rows or more", nflow >= 25000, nflow)
    meta = json.load(open(os.path.join(task, "metadata.json")))
    ok("gate: two or more distractors declared", len(meta["distractor_files"]) >= 2 and
       set(meta["distractor_files"]) == set(C.DISTRACTORS), meta["distractor_files"])
    ok("gate: no file name says distractor", not any("distract" in f.lower() for f in files))

    # ------------------------------------------------------------------ the call and its family
    ok("call: golden recomputes the generator's own free-float truth within 1.5 per cent",
       abs(g / W.free_truth() - 1) < 0.015, (round(g, 3), round(W.free_truth(), 3)))
    ok("call: the setting is 12", setting == 12, setting)
    fam = {k: res[k] for k in calc.GOLDEN_FAMILY}
    ok("call: every member of the instrument family rounds up to the setting", all(math.ceil(v) == setting for v in fam.values()),
       {k: round(v, 3) for k, v in fam.items()})
    ok("call: family spread under 4 per cent of the golden", (max(fam.values()) - min(fam.values())) / g < 0.04,
       round((max(fam.values()) - min(fam.values())) / g, 4))
    ok("call: golden at least 0.3 inside its bin (11, 12]", min(g - 11, 12 - g) >= 0.3, round(g, 3))
    ok("call: every family member at least 0.25 inside the bin", all(min(v - 11, 12 - v) >= 0.25 for v in fam.values()))
    for k in calc.RIVALS:
        ok("rival %s files a setting below 12 by at least one step" % k, math.ceil(res[k]) <= setting - 2 or
           (k in ("vol_reduced_form", "vol_no_bank_hours", "vol_variance_ratio", "vol_two_regressor_customer") and
            math.ceil(res[k]) <= setting - 1), (round(res[k], 3), math.ceil(res[k])))
    ok("rival: nearest rival at least 2.0 points under the golden",
       g - max(res[k] for k in calc.RIVALS) >= 2.0, round(g - max(res[k] for k in calc.RIVALS), 3))

    # resampling: one sigma of the impact over hour bootstraps, the sessions held (the estimand is the base years' own)
    rec = calc.Record(target)
    rng = np.random.default_rng(178)
    n = len(rec.r)
    boots = []
    for _ in range(80):
        pick = rng.integers(0, n, n)
        lam = calc.iv_slope(rec.r[pick], (rec.f - rec.i)[pick], rec.f[pick])
        boots.append(rec.vol(lam))
    sd = float(np.std(boots))
    ok("call: one sigma of the golden over 80 hour bootstraps of the impact leaves the setting at 12",
       math.ceil(g - sd) == 12 and math.ceil(g + sd) == 12, (round(g, 3), round(sd, 3)))
    ok("call: two sigma too", math.ceil(g - 2 * sd) == 12 and math.ceil(g + 2 * sd) == 12, (round(g, 3), round(sd, 3)))

    # ------------------------------------------------------------------ the three rules on the clean truth (R1 to R3)
    P, I, _ = W.bank()
    R, on, _ = W.path()
    F = W.total_flow_m()
    ok("R1 raw material: the hourly flows, operations and mids ship and the deciding impact is no shipped column",
       all(f in files for f in (C.F_FLOWS, C.F_OPS, C.F_MID)) and
       not any("impact" in h for h in open(os.path.join(target, C.F_FLOWS)).readline().split(",")))
    r_, f_, i_ = R.ravel(), F.ravel(), I.ravel()
    lam_ols = calc.ols_slope(r_, f_ - i_)
    lam_iv = calc.iv_slope(r_, f_ - i_, f_)
    d_clean = on + R.sum(axis=1)
    bank_day = I.sum(axis=1)
    v = lambda lam: math.sqrt(C.ANN * np.mean((d_clean + lam * bank_day) ** 2))
    ok("R3a analyst test: on the clean truth the net-flow regression puts the Bank back at a setting of 8",
       math.ceil(v(lam_ols)) == 8, round(v(lam_ols), 3))
    ok("R3a analyst test: the record alone files 7 on the clean truth", math.ceil(v(0.0)) == 7, round(v(0.0), 3))
    ok("R3b decisive step alone: the same route with customer flow as the instrument files 12 on the clean truth",
       math.ceil(v(lam_iv)) == 12, round(v(lam_iv), 3))
    lam_rf = calc.ols_slope(r_, f_)
    ok("R3b lower rung: the reduced form alone stays on 9", math.ceil(v(lam_rf)) == 9, round(v(lam_rf), 3))
    ok("R3 the Bank's trades answer the hour's own news (the reason the net-flow regression fails)",
       np.corrcoef(i_[i_ != 0], (P - W.LAMBDA * F).ravel()[i_ != 0])[0, 1] > 0.3)
    ok("R3 customer flow is independent of the hour's news", abs(np.corrcoef(f_, (P - W.LAMBDA * F).ravel())[0, 1]) < 0.03)
    ok("R3c no plant: no hourly flow series repeats a block of 24 hours", repeated_blocks(target) == 0)
    # R2: each mess item mishandled leaves the call where it was
    for label, kw in (("resubmissions summed", dict(resubmissions="sum")), ("first report kept", dict(resubmissions="first")),
                      ("Tres Valles' July 2025 reports kept", dict(fam_july="keep")),
                      ("ANULADA operations kept", dict(cancelled="keep"))):
        r2 = calc.call(target, **kw)
        ok("R2 mess neutral (%s): the golden route still files 12" % label, r2["setting"] == 12, round(r2["golden"], 3))
    ok("R2 the call's files share one clock and one unit (local hours, thousands of dollars), so no conversion sits "
       "on the call's path", open(os.path.join(target, C.F_OPS)).readline().split(",")[4] == "amount_usd_k")

    # ------------------------------------------------------------------ the semantic fork table, row by row
    dch = rec.dchg + res["impacts"]["iv_hourly"] * rec.dbank
    sd_demeaned = math.sqrt(C.ANN) * float(np.std(dch, ddof=1))
    ok("SF1 volatility as a demeaned standard deviation files the same setting", math.ceil(sd_demeaned) == 12, round(sd_demeaned, 3))
    cl = np.array([rec.close[d] for d in rec.days])
    simple = 100 * (cl[1:] / cl[:-1] - 1)
    adj = simple + res["impacts"]["iv_hourly"] * rec.dbank
    ok("SF1 simple rather than log changes file the same setting", math.ceil(math.sqrt(C.ANN * np.mean(adj ** 2))) == 12)
    nd = len(rec.days)
    hsq = np.zeros(nd)
    np.add.at(hsq, rec.day_of, (rec.r + res["impacts"]["iv_hourly"] * rec.i) ** 2)
    onr = np.array([100 * math.log(rec.open[rec.days[k]] / rec.close[rec.days[k - 1]]) for k in range(1, nd)])
    rv = math.sqrt(C.ANN * np.mean(hsq[1:] + onr ** 2))
    ok("SF1 a realised variance from hourly squares plus the overnight files the same setting", math.ceil(rv) == 12, round(rv, 3))
    ok("SF2 the sessions of 2024 to 2026 are the release's sessions, 2 January 2024 to 29 December 2026",
       rec.days[0] == C.FIRST_DAY and rec.days[-1] == C.LAST_DAY)
    pol = pdf_text(os.path.join(target, C.F_POLICY))
    ok("SF3 the counterfactual is filed once, in the pricing policy", norm_ws(D.ESTIMAND) in norm_ws(pol), D.ESTIMAND[:60])
    ok("SF4 customers exclude dealers and the Bank (release note section 2)",
       "Customers are all counterparties other than reporting dealers and the Bank" in norm_ws(pdf_text(os.path.join(target, C.F_NOTE))))
    ok("SF5 ANULADA operations kept or dropped, the setting holds", calc.call(target, cancelled="keep")["setting"] == 12)
    ok("SF6 operation stamps are local time like the dealers' hours (release note sections 1 and 2)",
       "time of the deal, local time" in norm_ws(pdf_text(os.path.join(target, C.F_NOTE))))
    ok("SF7 resubmissions: last received is of record; summed or first files the same setting",
       calc.call(target, resubmissions="sum")["setting"] == 12 and calc.call(target, resubmissions="first")["setting"] == 12)
    ok("SF8 Financiera Tres Valles of record to 30 June 2025; kept, the setting holds", calc.call(target, fam_july="keep")["setting"] == 12)
    ok("SF9 hours with a missing mark joined to the next or dropped file the same setting", drop_outage_setting(rec, res) == 12)
    ok("SF10 rounded up to the next whole per cent (policy section 2)", norm_ws(D.ROUND_UP) in norm_ws(pol))
    ok("SF11 the closing rate is the 16:00 mark (release note section 3, policy section 1)",
       "16:00 is the session close and the closing rate" in norm_ws(pdf_text(os.path.join(target, C.F_NOTE))))
    trm_vol = trm_volatility(target, res)
    ok("SF12 the options settle on the 16:00 closing rate, not the TRM (policy section 1); the TRM's recorded changes "
       "run under the close's", "cash settled against the platform's 16:00 closing rate" in norm_ws(pol) and trm_vol < res["record_vol"],
       round(trm_vol, 3))

    # ------------------------------------------------------------------ ask A
    a, n_orders = calc.ask_a(target)
    ok("ask A: 16 cells, every quarter and band", len(a) == 16, len(a))
    per_fill, _ = calc.ask_a(target, grouping="fill")
    hits = sum(1 for k in a if k in per_fill and round(per_fill[k], 1) == round(a[k], 1))
    ok("ask A device: executions read as orders miss every cell", hits == 0, hits)
    keepc, _ = calc.ask_a(target, drop_cancelled=False)
    ok("ask A hazard: CANCELLED rows kept move at least four cells",
       sum(1 for k in a if round(keepc[k], 1) != round(a[k], 1)) >= 4)
    keys = Counter()
    for r in csv.DictReader(open(os.path.join(target, C.F_CONF))):
        if r["status"] == "CONFIRMED":
            keys[(r["trader"], r["side"], r["trade_time_utc"])] += 1
    multi = sum(1 for v in keys.values() if v > 1)
    ok("ask A: orders with more than one execution are a minority of orders", 0.1 < multi / len(keys) < 0.6,
       round(multi / len(keys), 3))
    ok("ask A: every cell at least 0.009 from its rounding edge", all(C.edge(x, 0.1) >= 0.009 for x in a.values()),
       min(round(C.edge(x, 0.1), 4) for x in a.values()))
    ok("ask A: no band repeats one value in all four quarters",
       all(len({round(a[(q, b[0])], 1) for q in range(1, 5)}) > 1 for b in C.SIZE_BANDS))
    # ------------------------------------------------------------------ ask B
    sell, buy, _, nd_ = calc.ask_b(target)
    nsell, nbuy, _, _ = calc.ask_b(target, net_windows=False)
    ok("ask B device: window forwards left gross miss every figure",
       all(round(nsell[q], 1) != round(sell[q], 1) and round(nbuy[q], 1) != round(buy[q], 1) for q in range(1, 5)))
    esell, ebuy, _, _ = calc.ask_b(target, usd_only=False)
    ok("ask B hazard: euro deals kept move at least four figures",
       sum(1 for q in range(1, 5) for x, y in ((esell, sell), (ebuy, buy)) if round(x[q], 1) != round(y[q], 1)) >= 4)
    ok("ask B: no figure on a rounding tie (notionals are multiples of 5,000 dollars, so the nearest non-tie is 0.005)",
       all(C.edge(x, 0.1) >= 0.004 for x in list(sell.values()) + list(buy.values())),
       min(round(C.edge(x, 0.1), 4) for x in list(sell.values()) + list(buy.values())))
    ok("ask B: drawdowns found by client, side, rate and window equal the generator's own", nd_ == sum(
        1 for d in W.forward_book() if d["parent"] is not None and not d["cancelled"]
        and W.clients_by_no()[d["client"]]["segment"] != "TESORERIA"), nd_)

    # ------------------------------------------------------------------ separation: no ask device row in the call's population
    tmp = tempfile.mkdtemp(prefix="t178_sep_")
    try:
        for x in (C.F_FLOWS, C.F_OPS, C.F_MID, C.F_DEALERS, C.F_CAL):
            shutil.copy(os.path.join(target, x), tmp)
        r = calc.call(tmp)
        ok("separation: the call computed from the flows, operations, mids, dealer register and calendar alone is the "
           "golden to the last digit (no ask file is read)", r["golden"] == g and r["setting"] == setting)
        for x in os.listdir(tmp):
            os.remove(os.path.join(tmp, x))
        for x in (C.F_CONF, C.F_FWD, C.F_CLIENTS):
            shutil.copy(os.path.join(target, x), tmp)
        aa, _ = calc.ask_a(tmp)
        bb = calc.ask_b(tmp)
        ok("separation: both asks computed from their own three files alone, none the call reads", aa == a and
           bb[0] == sell and bb[1] == buy)
    finally:
        shutil.rmtree(tmp)

    # ------------------------------------------------------------------ distractors: deleting each moves nothing
    for f in C.DISTRACTORS:
        tmp = tempfile.mkdtemp(prefix="t178_dist_")
        try:
            for x in files:
                if x != f:
                    shutil.copy(os.path.join(target, x), tmp)
            r = calc.call(tmp)
            aa, _ = calc.ask_a(tmp)
            bb = calc.ask_b(tmp)
            ok("distractor %s deleted: call and asks unchanged" % f, r["setting"] == setting and abs(r["golden"] - g) < 1e-9
               and aa == a and bb[0] == sell and bb[1] == buy)
        finally:
            shutil.rmtree(tmp)

    # ------------------------------------------------------------------ figures.json and the write-up
    ok("figures: the call key", figs["call"]["pricing_volatility_pct"] == 12)
    ok("figures: every ask A cell as computed", all(figs["ask_a_hedging_cost_tqp_per_usd"]["Q%d" % q][b[0]] == round(a[(q, b[0])], 1)
                                                    for q in range(1, 5) for b in C.SIZE_BANDS))
    ok("figures: every ask B figure as computed", all(figs["ask_b_forwards_due_2027_usd_mn"]["Q%d" % q]["exporters_sell"] == round(sell[q], 1)
                                                      and figs["ask_b_forwards_due_2027_usd_mn"]["Q%d" % q]["importers_buy"] == round(buy[q], 1)
                                                      for q in range(1, 5)))
    sub = open(os.path.join(task, "submission.md")).read()
    ok("write-up: no em or en dash", "—" not in sub and "–" not in sub)
    ok("write-up: five blocks", [l for l in sub.splitlines() if l.startswith("## ")] ==
       ["## Tags", "## 1. Final Recommendation", "## 2. Critical Components", "## 3. Step-by-Step Solution", "## 4. Deliverable Answers"])

    # ------------------------------------------------------------------ documents read back (positive controls through the same extractor)
    for f, doc in D.DOCS.items():
        t = norm_ws(pdf_text(os.path.join(target, f)))
        ok("document %s reads back (control: its title)" % f, len(t) > 500 and norm_ws(doc["title"]) in t)
        ok("document %s: no ReportLab banner" % f, b"ReportLab" not in open(os.path.join(target, f), "rb").read())
    alltext = " ".join(norm_ws(pdf_text(os.path.join(target, f))) for f in D.DOCS)
    ok("leak control: the extractor finds a sentence that is there", "interbank platform" in alltext)
    for word in ("instrument", "endogen", "simultane", "price impact", "regress", "lean", "drawdown", "sweep", "execution per"):
        ok("leak: no document says %r" % word, word not in alltext.lower())

    # ------------------------------------------------------------------ dates and realism
    ok("dates: no Bank operation after the last session", max_utc_date(target) <= C.LAST_DAY + dt.timedelta(days=1))
    ok("dates: no dealer report received after the release", max_received(target) < dt.datetime.combine(C.RELEASE, dt.time(0)) + dt.timedelta(days=1))
    ok("dates: no confirmation outside 2026", conf_years(target) == {2026})
    ok("realism: dealer hourly figures are not round thousands", round_share(target) < 0.02, round(round_share(target), 4))
    ok("realism: the Bank dealt in between a fifth and a half of the hours", 0.2 < float((W.bank()[1] != 0).mean()) < 0.5,
       round(float((W.bank()[1] != 0).mean()), 3))
    card = json.load(open(os.path.join(os.path.dirname(task), ".claude", "skills", "fingerprint", "cards", "task178.json")))
    people = set(card["world"]["people"])
    ok("realism: the people the documents name are the card's", all(p in people for p in ("Yanet Cáceres", "Miguel Rengifo", "Inés Quiroz")))

    bad = [r for r in RESULTS if not r[1]]
    print("\n%d checks, %d failed" % (len(RESULTS), len(bad)))
    for r in bad:
        print("  FAILED:", r[0], r[2])
    return 1 if bad else 0


def repeated_blocks(target):
    vals = defaultdict(list)
    for r in csv.DictReader(open(os.path.join(target, C.F_FLOWS))):
        vals[r["dealer_code"]].append(int(r["net_customer_usd_k"]))
    n = 0
    for code, v in vals.items():
        seen = set()
        for k in range(0, len(v) - 24, 24):
            blk = tuple(v[k:k + 24])
            if blk in seen and any(blk):
                n += 1
            seen.add(blk)
    return n


def drop_outage_setting(rec, res):
    lost = {d for d, _ in W.OUTAGES}
    keep = np.array([rec.days[k] not in lost for k in rec.day_of])
    lam = calc.iv_slope(rec.r[keep], (rec.f - rec.i)[keep], rec.f[keep])
    return math.ceil(rec.vol(lam))


def trm_volatility(target, res):
    rows = list(csv.DictReader(open(os.path.join(target, C.F_TRM))))
    v = {dt.date.fromisoformat(r["fecha_vigencia"]): float(r["trm_tqp_per_usd"]) for r in rows}
    rec = calc.Record(target)
    seq = []
    for d in rec.days:
        nxt = d + dt.timedelta(days=1)
        seq.append(v.get(nxt, np.nan))
    seq = np.array(seq)
    ch = 100 * np.diff(np.log(seq))
    ch = ch[~np.isnan(ch)]
    return math.sqrt(C.ANN * np.mean(ch ** 2))


def max_utc_date(target):
    return max(dt.datetime.strptime(r["dealt_at"], "%Y-%m-%d %H:%M:%S").date()
               for r in csv.DictReader(open(os.path.join(target, C.F_OPS))))


def max_received(target):
    return max(dt.datetime.strptime(r["received_at"], "%Y-%m-%d %H:%M:%S") for r in csv.DictReader(open(os.path.join(target, C.F_FLOWS))))


def conf_years(target):
    return {int(r["trade_time_utc"][:4]) for r in csv.DictReader(open(os.path.join(target, C.F_CONF)))}


def round_share(target):
    v = [int(r["net_customer_usd_k"]) for r in csv.DictReader(open(os.path.join(target, C.F_FLOWS)))]
    return sum(1 for x in v if x != 0 and x % 1000 == 0) / len(v)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
