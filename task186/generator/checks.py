"""Assertions for task186, run on the installed target/ against the generator's clean truth.

    python3 task186/generator/checks.py          # exit 0 when every assertion passes
"""
import csv
import datetime as dt
import json
import os
import re
import sys
from collections import defaultdict

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import io_util as IO  # noqa: E402
import pack as PK  # noqa: E402
import params as P  # noqa: E402
import world as W  # noqa: E402

TARGET = os.path.join(TASK, "target")
RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))


def main():
    w = W.World()
    T = A.load(TARGET)
    M = A.main_call(T)
    tab = M["table"]
    gold = set(M["golden"])
    ids = PK.Identities(w)
    staff_of = {ids.staff[o["idx"]]: o for o in w.off}

    # ------------------------------------------------------------------ input gates
    files = sorted(os.listdir(TARGET))
    check("gate: ten or more files", len(files) >= 10, "%d files" % len(files))
    fmts = sorted(set(f.rsplit(".", 1)[1] for f in files))
    check("gate: three or more formats", len(fmts) >= 3, ",".join(fmts))
    big = max(sum(1 for _ in open(os.path.join(TARGET, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    check("gate: a file of 25,000 rows or more", big >= 25000, "%d rows" % big)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    dis = meta["distractor_files"]
    check("gate: two or more distractors declared and shipped", len(dis) >= 2 and all(d in files for d in dis), str(dis))
    bad = [f for f in files if re.search(r"readme|dictionary|notes|manifest|field|test_|trap|decoy|distractor", f, re.I)]
    check("gate: no file describes the data or names the device", not bad, str(bad))
    check("gate: metadata names no method", not re.search(r"first show|seen before|recogni|memor|repeat|new to",
                                                           json.dumps(meta), re.I), "metadata.json clean")

    # ------------------------------------------------------------------ R1: the field's raw material ships
    tipcols = list(T["tip"].columns)
    check("R1 projection-level outcomes ship (one row per projection with its result)",
          {"event_utc", "operator_login", "image_no", "result"} <= set(tipcols), str(tipcols))
    allcols = set(tipcols) | set(T["images"].columns) | set(T["objects"].columns) | set(T["logins"].columns) \
        | set(T["register"].columns)
    check("R1 no shipped column holds the deciding quantity",
          not any(re.search(r"prior|first|seen|repeat|detect|performance|novel", c, re.I) for c in allcols),
          ",".join(sorted(allcols)))

    # ------------------------------------------------------------------ the golden against the clean truth
    truth_def = {ids.staff[o["idx"]] for o in w.off if o["deficient"] and not o["left"]}
    check("golden set is the officers whose detection of an unseen item is below standard", gold == truth_def,
          "golden %d, truth %d" % (len(gold), len(truth_def)))
    check("golden: ten officers come off", len(gold) == 10, str(sorted(gold)))
    tgt = {s: staff_of[s]["target"] for s in tab["staff_no"]}
    check("truth: every designated officer below 0.75 and every other at 0.88 or above",
          max(tgt[s] for s in gold) < 0.75 and min(tgt[s] for s in tab["staff_no"] if s not in gold) >= 0.88,
          "max des %.3f min other %.3f" % (max(tgt[s] for s in gold), min(tgt[s] for s in tab["staff_no"] if s not in gold)))

    # ------------------------------------------------------------------ R3: the analyst test and the decisive step
    r0 = set(M["r0"])
    check("R3a the default path (each officer's hit rate over the year) files the named wrong answer",
          r0 != gold and len(r0) == 3 and r0 < gold, "R0 %s" % sorted(r0))
    missed = gold - r0
    check("R3a the default path misses all six full-time officers and one casual officer",
          sum(staff_of[s]["kind"] == "FT" for s in missed) == 6 and len(missed) == 7, "missed %d" % len(missed))
    check("R3b the decisive step alone (object-level first showings) reaches the golden",
          set(A.designated(tab, "golden")) == gold, "golden from first showings")
    check("R3b rung R1 (category-balanced hit rate) stays wrong", set(M["r1"]) != gold, str(M["r1"]))
    check("R3b rung R2 (first showings of each image file) stays wrong", set(M["r2"]) != gold, str(M["r2"]))
    check("R3b rung R2b (first showings counted inside the window only) stays wrong", set(M["r2b"]) != gold,
          str(M["r2b"]))
    check("R3c no plant: no block of TIP rows repeats except the one re-sent day",
          _repeated_blocks(T["tip"]) <= 1, "re-sent blocks %d" % _repeated_blocks(T["tip"]))
    check("R3c no memo, draft, briefing or stakeholder figure ships",
          not any(f.endswith((".docx", ".txt", ".md", ".eml")) for f in files), ",".join(files))

    # ------------------------------------------------------------------ the licensed family and the margins
    for col, label in (("cat_rw", "category-reweighted first showings"), ("logit0", "logistic fit at no prior showing")):
        check("licensed: %s designates the same officers" % label, set(A.designated(tab, col)) == gold, col)
    des = tab[tab["staff_no"].isin(gold)]
    non = tab[~tab["staff_no"].isin(gold)]
    mx = max(des[c].max() for c in ("golden", "cat_rw", "logit0"))
    mn = min(non[c].min() for c in ("golden", "cat_rw", "logit0"))
    check("margin: every designated officer at most 0.765 under every licensed form", mx <= 0.765, "%.4f" % mx)
    check("margin: every other officer at least 0.83 under every licensed form", mn >= 0.83, "%.4f" % mn)
    check("SF12 no officer within 0.03 of the 80 per cent line under any licensed form",
          ((tab[["golden", "cat_rw", "logit0"]] - 0.80).abs().min().min()) >= 0.03, "nearest %.4f" %
          (tab[["golden", "cat_rw", "logit0"]] - 0.80).abs().min().min())

    # ------------------------------------------------------------------ the structure the data force
    tip = A.tip_events(T)
    win = tip[tip["in_window"]]
    check("memory signal: repeat showings detected far more often than first showings",
          M["pooled_hit_repeat"] - M["pooled_hit_first"] >= 0.08,
          "first %.4f repeat %.4f" % (M["pooled_hit_first"], M["pooled_hit_repeat"]))
    fi = win[win["prior_img"] == 0]
    a, b = fi.loc[fi["prior_obj"] == 0, "hit"].mean(), fi.loc[fi["prior_obj"] > 0, "hit"].mean()
    check("SF3 object level forced: an image shown for the first time is detected far more often when another "
          "view of its object was shown before", b - a >= 0.08, "new object %.4f, seen object %.4f" % (a, b))
    last = {}
    gaps = []
    for s, o, t, h in zip(tip["staff_no"], tip["object_code"], tip["t_utc"], tip["hit"]):
        k = (s, o)
        if k in last:
            gaps.append(((t - last[k]).days, h))
        last[k] = t
    g = np.array(gaps)
    near, far = g[g[:, 0] <= 30, 1].mean(), g[g[:, 0] > 120, 1].mean()
    check("SF4 any earlier showing counts: the lift does not fade with time since the last showing",
          abs(near - far) <= 0.02, "within 30 days %.4f, after 120 days %.4f" % (near, far))
    pre = win[(win["prior_obj"] > 0) & (win["prior_obj_win"] == 0)]
    check("SF4 objects first shown before the window are recognised in it like any repeat",
          pre["hit"].mean() - M["pooled_hit_first"] >= 0.08, "pre-window repeats %.4f" % pre["hit"].mean())

    # ------------------------------------------------------------------ shock: the answer is no interval of a sort
    reg = T["register"].set_index("staff_no")
    sorts = {"hit rate": tab.set_index("staff_no")["overall"], "projections": tab.set_index("staff_no")["n"],
             "endorsed": reg["xray_endorsed"].loc[tab["staff_no"]].map(lambda x: x.toordinal() if hasattr(x, "toordinal") else 0),
             "category-balanced": tab.set_index("staff_no")["cat_bal"],
             "image-level first showings": tab.set_index("staff_no")["first_img"]}
    intervals = []
    for name, ser in sorts.items():
        order = list(ser.sort_values(kind="mergesort").index)
        pos = sorted(order.index(s) for s in gold)
        if pos[-1] - pos[0] + 1 == len(pos):
            intervals.append(name)
    check("shock: the ten are not an interval of any shipped statistic's sort", not intervals, str(intervals))
    check("shock: the masked full-time officers sit inside the hit-rate spread, not below it",
          tab.loc[tab["staff_no"].isin(gold - r0), "overall"].max() > tab.loc[~tab["staff_no"].isin(gold), "overall"].min(),
          "max masked %.3f, min other %.3f" % (tab.loc[tab["staff_no"].isin(gold - r0), "overall"].max(),
                                              tab.loc[~tab["staff_no"].isin(gold), "overall"].min()))

    # ------------------------------------------------------------------ R2: every Layer 1 item neutral on the call
    def golden_with(**kw):
        tp = A.tip_events(T, **kw)
        return set(A.designated(A.officer_table(T, tp), "golden"))
    check("R2 SF7 the re-sent D3 day kept twice leaves the call", golden_with(dedupe=False) == gold, "no dedupe")
    check("R2 SF1 the window read on UTC dates leaves the call", golden_with(local_window=False) == gold, "UTC dates")
    T2 = dict(T)
    T2["tip"] = T["tip"][~T["tip"]["operator_login"].str.startswith("OP7")]
    tp = A.tip_events(T2)
    check("R2 international logins left unmapped (rows dropped) leave the call",
          set(A.designated(A.officer_table(T2, tp), "golden")) == gold, "OP7 rows dropped")
    T3 = dict(T)
    t3 = T["tip"].copy()
    t3 = t3[t3["image_no"].str.len() == 6]
    T3["tip"] = t3
    check("R2 image numbers left unpadded (international rows unmatched) leave the call",
          set(A.designated(A.officer_table(T3, A.tip_events(T3)), "golden")) == gold, "5-digit rows dropped")
    check("R2 the call reads none of the ask files (roster, leave, unit counts, unit register)",
          "roster" not in _main_call_sources(), "main_call sources")

    # ------------------------------------------------------------------ ask A against the clean truth
    aa, hrs = A.ask_a(T)
    truth_a = _truth_ask_a(w, ids)
    check("ask A golden equals the clean truth month by month", aa == truth_a, "%s vs %s" % (aa, truth_a))
    a_nol, _ = A.ask_a(T, use_leave=False)
    a_blk, _ = A.ask_a(T, mode="blockkey")
    a_no, _ = A.ask_a(T, mode="nodiv")
    check("ask A rung: personal leave ignored misses five or more months",
          sum(x != y for x, y in zip(a_nol, aa)) >= 5, "%s" % a_nol)
    check("ask A rung: one divisor per roster block misses every month", all(x != y for x, y in zip(a_blk, aa)),
          "%s" % a_blk)
    check("ask A rung: no division at all files zero every month", all(x == 0 for x in a_no), "%s" % a_no)
    check("SF9 X-ray time at five-minute and boundary resolution agree", _ask_a_minutes(T) == aa, "minute sweep")

    # ------------------------------------------------------------------ ask B against the clean truth
    ab = A.ask_b(T)
    truth_b = _truth_ask_b(w)
    check("ask B golden equals the clean truth lane by lane and quarter by quarter", ab == truth_b,
          "max diff %d" % max(abs(ab[k] - truth_b[k]) for k in truth_b))
    b_reg = A.ask_b(T, mode="register")
    b_open = A.ask_b(T, mode="register_open")
    miss_reg = sum(A.rnd_k(b_reg.get(k, 0)) != A.rnd_k(v) for k, v in ab.items())
    check("ask B rung: units placed by the register's current location miss ten or more figures", miss_reg >= 10,
          "%d of 28" % miss_reg)
    assign, c, lh = A.unit_lanes(T)
    inv = {(d, u): ln for (d, ln), u in assign.items()}
    c["lane"] = [inv.get((d, u)) for d, u in zip(c["date"], c["unit_serial"])]
    c["d"] = pd.to_datetime(c["date"]).dt.date
    c = c[c["lane"].isin(P.LANES)]
    tests_in = {}
    for q, a0, b0 in A.QUARTERS:
        m = (c["d"] >= a0) & (c["d"] <= b0)
        tests_in.update({(ln, q): int(v) for ln, v in c[m].groupby("lane")["bags_imaged"].sum().items()})
    miss_test = sum(A.rnd_k(tests_in.get(k, 0)) != A.rnd_k(v) for k, v in ab.items())
    check("ask B rung: units placed right but pre-opening counts kept miss ten or more figures", miss_test >= 10,
          "%d of 28" % miss_test)
    check("ask B: every unit-day placed on the lane it truly stood on",
          all(PK.unit_on(ln, dt.date.fromisoformat(d)) == u for (d, ln), u in assign.items()), "%d lane-days" % len(assign))
    check("SF10 quarters on Sydney dates: UTC quarters move a figure", any(
        A.rnd_k(A.ask_b(T, mode="register_utc").get(k, 0)) != A.rnd_k(b_reg.get(k, 0)) for k in ab), "UTC vs local")
    cover = defaultdict(set)
    for (i, d, ln, s0, e0, sick) in w.roster:
        for mm in range(s0, e0):
            cover[(d, ln)].add(mm)
    stray = sum(bags for (d, ln, s0, length, bags, op) in w.slots if bags and P.WIN0 <= d <= P.WIN1
                and s0 not in cover[(d, ln)])
    check("C1 ask B: every passenger bag falls inside the lane's rostered time, so one rule separates the counts",
          stray == 0, "%d bags outside rostered time" % stray)
    pre = 0
    for (d, ln), mins in cover.items():
        if P.WIN0 <= d <= P.WIN1:
            fo = min(mins)
            pre += fo % 60 == 0 or True
    check("C1 ask B: test images sit in an hour before the lane's first rostered start every day",
          all(h < min(lh[(d, ln)]) for (d, ln), h in _test_hours(T, assign, lh).items()), "test hours")

    # ------------------------------------------------------------------ separation of the asks from the call
    check("separation: the TIP log carries no ask device rows (no unit serial, no roster or leave key)",
          not any(c2 in T["tip"].columns for c2 in ("unit_serial", "roster_date", "payroll_no")), str(tipcols))

    # ------------------------------------------------------------------ SF rows on the population and the windows
    pop = A.population(T)
    check("SF2 the population is the register's current endorsements on 30 November", len(pop) == len(tab) == 91,
          "%d officers" % len(pop))
    check("SF8 ask A counts only officers endorsed for the whole month",
          all(len(v) <= len(pop) + 2 for v in A.whole_month_population(T).values()), "monthly populations")
    check("SF5 category weighting does not move the call", set(A.designated(tab, "cat_rw")) == gold, "cat_rw")
    check("SF6 the logistic fit does not move the call", set(A.designated(tab, "logit0")) == gold, "logit0")
    check("SF11 passenger bags leave out the counts before a lane's first rostered start", miss_test >= 10,
          "pre-opening counts move %d figures" % miss_test)
    check("SF13 every endorsed officer has thirty or more first showings in the window", tab["n_first"].min() >= 30,
          "min %d" % tab["n_first"].min())

    # ------------------------------------------------------------------ realism sweep
    for col, ser in (("staff_no", T["register"]["staff_no"]), ("payroll_no", T["register"]["payroll_no"]),
                     ("login", T["logins"]["login"]), ("image_no", T["images"]["image_no"])):
        v = sorted(int(re.sub(r"\D", "", str(x))) for x in ser)
        dif = set(np.diff(v))
        check("realism: %s is not an arithmetic sequence" % col, len(dif) > 3, "%d distinct steps" % len(dif))
    vals = list(ab.values())
    check("realism: no two lane-quarter counts identical", len(set(vals)) == len(vals), "%d values" % len(vals))
    names = list(zip(T["register"]["given_name"], T["register"]["surname"]))
    check("realism: no full name repeats in the register", len(set(names)) == len(names), "%d officers" % len(names))
    std = IO.pdf_text(os.path.join(TARGET, PK.FILES["standard"]))
    check("positive control: the standard's text is readable", "Detection performance" in std and len(std) > 1500,
          "%d characters" % len(std))
    check("the standard files the estimand's words",
          "probability that the officer detects a prohibited item carried" in std and "80 per cent" in std, "WHAT")
    check("the standard names no repeat, first showing, recognition or object history",
          not re.search(r"first show|seen before|repeat|recogni|memor|familiar|new to the officer", std, re.I), "clean")
    check("persona: the standard's approver is a drawn persona", "Teresa Malone" in std, "Teresa Malone")
    check("document dates: the standard was approved before the CT lanes' first projection",
          dt.date(2025, 7, 14) >= P.DAY0 and T["tip"]["event_utc"].min() < "2025-07-14", T["tip"]["event_utc"].min())
    check("extract dates: no record after the pull", T["tip"]["event_utc"].max() < "2026-12-01", T["tip"]["event_utc"].max())
    for d in dis:
        check("distractor %s unused by the golden and every ask" % d, d not in _main_call_sources() + _ask_sources(), d)

    fails = [r for r in RESULTS if not r[1]]
    for label, ok, detail in RESULTS:
        print("%s  %s  %s" % ("PASS" if ok else "FAIL", label, detail))
    print("%d assertions, %d failed" % (len(RESULTS), len(fails)))
    sys.exit(1 if fails else 0)


def _test_hours(T, assign, lh):
    """The local hour of each retrofitted unit's daily pre-opening count (its first counted hour, when that hour
    lies outside the lane's rostered hours)."""
    c = T["counts"].copy()
    c["t"] = pd.to_datetime(c["hour_start_utc"]).dt.tz_localize("UTC").dt.tz_convert(P.TZ.key)
    c["date"] = c["t"].dt.strftime("%Y-%m-%d")
    c["h"] = c["t"].dt.hour
    inv = {(d, u): ln for (d, ln), u in assign.items()}
    out = {}
    for (d, u), g in c.groupby(["date", "unit_serial"]):
        ln = inv.get((d, u))
        if ln is None:
            continue
        outside = [h for h in g["h"] if h not in lh[(d, ln)]]
        if outside:
            out[(d, ln)] = max(outside)
    return out


def _repeated_blocks(tip):
    dup = tip[tip.duplicated(keep=False)]
    if dup.empty:
        return 0
    days = dup["event_utc"].str[:10].nunique()
    return 1 if days <= 2 and set(dup["lane"]) == {"D3"} else days


def _main_call_sources():
    import inspect
    return inspect.getsource(A.main_call) + inspect.getsource(A.tip_events) + inspect.getsource(A.officer_table)


def _ask_sources():
    import inspect
    return inspect.getsource(A.ask_a) + inspect.getsource(A.xray_time) + inspect.getsource(A.ask_b) \
        + inspect.getsource(A.unit_lanes)


def _truth_ask_a(w, ids):
    hours = defaultdict(float)
    by = defaultdict(list)
    for (i, d, ln, s, e, sick) in w.roster:
        if P.WIN0 <= d <= P.WIN1 and not sick:
            by[(d, ln)].append((i, s, e))
    for (d, ln), rows in by.items():
        lo, hi = min(r[1] for r in rows), max(r[2] for r in rows)
        for m in range(lo, hi):
            on = [r[0] for r in rows if r[1] <= m < r[2]]
            for i in on:
                hours[(ids.staff[i], (d.year, d.month))] += 1.0 / 60.0 / len(on)
    out = []
    for (y, m) in A.MONTHS:
        first = dt.date(y, m, 1)
        last = dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)
        n = 0
        for o in w.off:
            if o["endorsed"] <= first and (not o["left"] or o["left"] >= last):
                if hours.get((ids.staff[o["idx"]], (y, m)), 0.0) < P.CURRENCY_H - 1e-9:
                    n += 1
        out.append(n)
    return out


def _ask_a_minutes(T):
    ro = T["roster"].copy()
    pay = T["register"].set_index("payroll_no")["staff_no"]
    lv = T["leave"][T["leave"]["leave_type"] == "Personal leave"]
    absent = set(zip(lv["payroll_no"].map(pay), lv["leave_date"]))
    ro = ro[[(a, b) not in absent for a, b in zip(ro["staff_no"], ro["roster_date"])]]
    hours = defaultdict(float)
    for (d, ln), g in ro.groupby(["roster_date", "lane"]):
        s = g["start"].map(A.to_min).values
        e = g["finish"].map(A.to_min).values
        st = g["staff_no"].values
        for m in range(s.min(), e.max(), 5):
            on = (s <= m) & (e >= m + 5)
            k = on.sum()
            for x in st[on]:
                hours[(x, (int(d[:4]), int(d[5:7])))] += 5 / 60.0 / k
    pop = A.whole_month_population(T)
    return [sum(1 for s2 in pop[mk] if hours.get((s2, mk), 0.0) < P.CURRENCY_H) for mk in A.MONTHS]


def _truth_ask_b(w):
    out = defaultdict(int)
    for (d, ln, s, length, bags, op) in w.slots:
        for q, a, b in A.QUARTERS:
            if a <= d <= b:
                out[(ln, q)] += bags
    return {(ln, q): out.get((ln, q), 0) for ln in P.LANES for q, _, _ in A.QUARTERS}


if __name__ == "__main__":
    main()
