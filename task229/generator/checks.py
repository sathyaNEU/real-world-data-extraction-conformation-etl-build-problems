"""Every assertion task229's design owes, by name: the ladder sets and margins, SF1 to SF12, the rung-3
estimators' agreement, the grid cells, the clean-data and lens-swap tests, the ask devices and stops with
every composed subset, the cracker and mirror sheets, the pair ceiling, the input gates and the realism sweep.
Run by make.py on every build; any failure stops the build."""
import itertools
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W
import simulate as S
import estimate as E
import asks as A
import docs as DC
import build as B

GOLD = ["Avonmouth", "Bellshill", "Daventry", "Hinckley", "Magor", "Warrington"]
DISTINCT = ["Avonmouth", "Bellshill", "Daventry", "Warrington"]
LOG = []


def ok(cond, label):
    LOG.append(label)
    if not cond:
        raise AssertionError("FAILED: " + label)


def edge_dist(x):
    """Distance of x from the nearest whole-per-cent rounding edge (x.5)."""
    return abs((x - math.floor(x)) - 0.5)


def qual(est, key):
    return sorted(n for n in W.NAMES if est[n][key] >= W.LINE)


def main_path(target, world):
    est = E.everything(target)
    truth = S.truth(world["sim"])
    # the ladder, set by name
    ok(qual(est, "rung0_all_counts") == [], "rung 0 (all count tasks) qualifies no centre")
    ok(qual(est, "rung1_routine") == ["Magor"], "rung 1 (routine counts) qualifies Magor only")
    ok(qual(est, "rung2_class_weighted") == ["Hinckley", "Magor"], "rung 2 (class-weighted routine) qualifies Magor and Hinckley")
    for k in E.R3_KEYS:
        ok(qual(est, k) == GOLD, "rung 3 %s qualifies the six" % k)
    ok(qual(est, E.GOLDEN_KEY) == GOLD, "golden set (per day by class) is the six")
    # margins and positions
    for n in W.NAMES:
        e = est[n]
        vals = [e[k] for k in E.R3_KEYS]
        ok(all(abs(v - W.LINE) >= 0.6 for v in vals), "%s: every rung-3 estimator at least 0.6 from 97.0" % n)
        ok(all(edge_dist(v) >= 0.2 for v in vals), "%s: every rung-3 estimator at least 0.2 from an x.5 edge" % n)
        ok(len({round(v) for v in vals}) == 1, "%s: every rung-3 estimator gives the same whole per cent" % n)
        ok((truth[n] >= W.LINE + 0.6) == (n in GOLD) and abs(truth[n] - W.LINE) >= 0.6,
           "%s: private truth at least 0.6 from 97.0 on the golden's side" % n)
        ok(abs(e["rung1_routine"] - W.LINE) >= 0.5, "%s: rung 1 at least 0.5 from the line" % n)
        ok(e["rung0_all_counts"] <= W.LINE - 1.0, "%s: rung 0 at least 1.0 under the line" % n)
        for k in ("rung0_all_counts", "rung1_routine", "rung2_class_weighted", "cell_weighted_flag_class",
                  "latest_result_per_face"):
            ok(e[E.GOLDEN_KEY] - e[k] >= 0.5, "%s: C4 shortfall, %s at least 0.5 under the estimate (4.5)" % (n, k))
        for w in range(4, 27):
            ok(e[E.GOLDEN_KEY] - e["rung2_last_%dw" % w] >= 0.5, "%s: C4 shortfall, rung 2 over %d weeks at least 0.5" % (n, w))
        ok(e["counted_taken_as_correct"] > e[E.GOLDEN_KEY], "%s: over-correction stop sits above the estimate" % n)
    ok(est["Hinckley"]["rung1_routine"] <= 96.5, "first tuning item: Hinckley rung 1 at 96.5 or under (%.2f)" % est["Hinckley"]["rung1_routine"])
    ok(est["Hinckley"]["rung2_class_weighted"] >= 97.5, "first tuning item: Hinckley rung 2 at 97.5 or over (%.2f)" % est["Hinckley"]["rung2_class_weighted"])
    for w in range(4, 27):
        s = qual(est, "rung2_last_%dw" % w)
        ok(not set(DISTINCT) & set(s), "rung 2 over %d weeks qualifies none of the four distinctive centres" % w)
        ok(len(set(s) ^ set(GOLD)) >= 4, "rung 2 over %d weeks differs from the answer in four or more verdicts" % w)
        if w >= 8:
            ok(s == ["Hinckley", "Magor"], "rung 2 over %d weeks is Magor and Hinckley" % w)
    # grid and partial cells
    ok(qual(est, "cell_weighted_flag_class") == ["Magor"], "grid: counts weighted by flag-and-class cell give Magor")
    ok(qual(est, "latest_result_per_face") == ["Magor"], "grid: each face's latest count result gives Magor")
    ok(qual(est, "accrual_from_every_count") == ["Magor"], "grid: reset seen, accrual from every count, gives Magor")
    ok(qual(est, "resets_at_routine_only") == GOLD, "grid: resets at routine counts only converges on the six")
    for n in W.NAMES:
        ok(abs(est[n]["resets_at_routine_only"] - est[n][E.GOLDEN_KEY]) <= 0.25,
           "%s: resets-at-routine-only within 0.25 of the estimate" % n)
    ok(qual(est, "counted_taken_as_correct") == sorted(W.NAMES), "grid: a counted face taken as correct gives all eight")
    ok(qual(est, "per_day_pooled_classes") == ["Hinckley", "Magor"],
       "grid: per-day accrual pooled over classes (class hazards differ) gives rung 2's set")
    for n in W.NAMES:
        for k in ("rung1_routine", "rung2_class_weighted", "cell_weighted_flag_class", "latest_result_per_face",
                  "accrual_from_every_count", "per_day_pooled_classes"):
            ok(est[n][k] < est[n][E.GOLDEN_KEY], "%s: sign discipline, %s below the answer" % (n, k))
    return est


def semantic_forks(target, world, est):
    loc, cnt = E.load(target)
    faces = E.in_scope(loc)
    reg = pd.read_csv(os.path.join(target, S.FILES["centres"]), dtype=str)
    # SF1
    ok(len(reg) == 8 and set(reg.site) == {c["code"] for c in W.CENTRES}, "SF1: the centre register lists the eight centres")
    ok(set(cnt.site) <= set(reg.site) and set(faces.site) == set(reg.site), "SF1: no other site holds a Thornacre face")
    # SF2
    ok(qual(est, "rung0_all_counts") == [] and qual(est, E.GOLDEN_KEY) != [], "SF2: count-task share gives no centre")
    # SF3
    ok(((cnt.confirmed_qty.astype(int) == cnt.system_qty.astype(int)) == (cnt.result == "MATCH")).all(),
       "SF3: result is confirmed equals system on every row")
    f2, c2 = E.prepared(target)
    c2["hit"] = c2.variance_qty.astype(int).abs() <= 1
    loose = E.rung3(f2, c2)
    names = {c["code"]: c["name"] for c in W.CENTRES}
    loose_set = sorted(names[k] for k, v in loose.items() if v[E.GOLDEN_KEY] >= W.LINE)
    ok(set(loose_set) > set(GOLD), "SF3: the within-a-case reading passes more centres (%s)" % loose_set)
    ok("equals the quantity a count" in " ".join(t for _, t in DC.STANDARD), "SF3: 4.2 files 'equals'")
    # SF4, SF12
    st = " ".join(t for _, t in DC.STANDARD)
    ok("06:00 on 7 December 2026" in st and "4 January 2027" in st, "SF4/SF12: 4.4 and 5.1 file the moment and the freeze")
    ok(cnt.posted_utc.max() <= "2026-12-07T06:00:00Z", "SF4/SF10: the export closes at the stand-down")
    # SF5
    ok(qual(est, "rung2_class_weighted") == ["Hinckley", "Magor"], "SF5: any estimate from the count records (rung 2) gives Magor and Hinckley")
    # SF6 held faces counted in
    held = loc[(loc.location_type == "PICK") & (loc.client == "THN") & loc.status.isin(["HOLD", "RECALL"])
               & (loc.eff_to == "")]
    ok(len(held) > 0, "SF6: held faces exist at the stand-down (%d)" % len(held))
    ok(_golden_with(target, extra=held[["site", "location"]]) == _whole(est), "SF6: counting held faces in moves no verdict and no whole per cent")
    # SF7, SF8 are margins (main_path)
    # SF9 OVR read as routine
    f3, c3 = E.prepared(target)
    c3["routine"] = c3.reason_code.isin(["CYC", "OVR"])
    ok(_whole_from(E.rung3(f3, c3)) == _whole(est), "SF9: overflowed replenishment read as routine moves nothing")
    # SF10 last night left out
    f4, c4 = E.prepared(target)
    c4 = c4[c4.day < W.F - 1].copy()
    same = (c4.site == c4.site.shift()) & (c4.location == c4.location.shift())
    c4["age"] = np.where(same, c4.day - c4.day.shift(), np.nan)
    r4 = E.rung3(f4, c4)
    ok(sorted(names[k] for k, v in r4.items() if v[E.GOLDEN_KEY] >= W.LINE) == GOLD, "SF10: the last night left out gives the same six")
    # SF11
    m = cnt.merge(loc[loc.location_type == "PICK"][["site", "location"]].drop_duplicates(), on=["site", "location"], how="left", indicator=True)
    ok((m._merge == "both").all(), "SF11: every count row's site and location is on the location master")
    ins_rows = loc.merge(faces[["site", "location"]], on=["site", "location"])
    ins_rows = ins_rows[ins_rows.location_type == "PICK"]
    ok(ins_rows.groupby(["site", "location"]).size().max() == 1, "SF11: each in-scope face has one version through the window")
    ok((faces.eff_from < "2026-06-01").all(), "SF11/closure 5: every in-scope face slotted and classed before 1 June")
    # SF12
    days = sorted(pd.to_datetime(pd.Series(W.FREEZE_DAYS)).dt.strftime("%Y-%m-%d"))
    ok(days[0] == "2026-12-07" and days[-1] == "2027-01-03" and len(days) == 28, "SF12: the freeze's trading days are 7 December to 3 January")
    sf13_pooling(target, est, names)
    sf14_first_count(target, est, names)


def _wald(age, hit, p):
    """95 per cent Wald interval on the per-day hazard p from the observed information of the geometric likelihood."""
    age = np.asarray(age, float); hit = np.asarray(hit, bool)

    def ll(q):
        pr = np.clip((1 - q) ** age, 1e-12, 1 - 1e-12)
        return np.log(pr[hit]).sum() + np.log(1 - pr[~hit]).sum()
    h = p * 1e-3
    info = -(ll(p + h) - 2 * ll(p) + ll(p - h)) / h ** 2
    se = info ** -0.5
    return p - 1.96 * se, p + 1.96 * se


def sf13_pooling(target, est, names):
    """SF13: the per-day accrual pooled over the three classes gives rung 2's set, and the routine counts
    themselves rule pooling out: the per-day class hazards are separated with non-overlapping intervals at every
    centre, and the pooled hazard mis-predicts each class's own routine match rate."""
    ok(qual(est, "per_day_pooled_classes") == ["Hinckley", "Magor"], "SF13: per-day pooled over classes gives Magor and Hinckley")
    faces, c = E.prepared(target)
    obs = c[c.routine & c.age.notna()]
    for code, o in obs.groupby("site"):
        n = names[code]
        pk, iv = {}, {}
        for k in "ABC":
            ok_ = o[o.slot_class == k]
            pk[k] = E.fit_geom(ok_.age, ok_.hit)
            iv[k] = _wald(ok_.age, ok_.hit, pk[k])
        ok(iv["A"][0] > iv["B"][1] and iv["B"][0] > iv["C"][1],
           "SF13 %s: per-day class hazards separated, 95%% intervals A [%.5f, %.5f] > B [%.5f, %.5f] > C [%.5f, %.5f]"
           % (n, iv["A"][0], iv["A"][1], iv["B"][0], iv["B"][1], iv["C"][0], iv["C"][1]))
        ok(pk["A"] / pk["C"] >= 15, "SF13 %s: an A face goes wrong %.1f times as fast a day as a C face (15 or more)" % (n, pk["A"] / pk["C"]))
        pp = E.fit_geom(o.age, o.hit)
        gap = {}
        for k in "ABC":
            ok_ = o[o.slot_class == k]
            seen = 100 * ok_.hit.mean()
            gap[k] = 100 * ((1 - pp) ** ok_.age).mean() - seen
            fit_k = 100 * ((1 - pk[k]) ** ok_.age).mean() - seen
            ok(abs(fit_k) <= 0.1, "SF13 %s: the class-%s hazard reproduces the class's routine match rate within 0.1 (%+.2f)" % (n, k, fit_k))
        ok(gap["A"] >= 3.5, "SF13 %s: the pooled hazard over-predicts the A routine match rate by 3.5 or more (%+.2f)" % (n, gap["A"]))
        ok(gap["B"] <= -0.5, "SF13 %s: the pooled hazard under-predicts the B routine match rate by 0.5 or more (%+.2f)" % (n, gap["B"]))
        ok(gap["C"] <= -3.0, "SF13 %s: the pooled hazard under-predicts the C routine match rate by 3.0 or more (%+.2f)" % (n, gap["C"]))


def _docx_text(path):
    import docx
    d = docx.Document(path)
    parts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            parts.extend(cell.text for cell in row.cells)
    return " ".join(parts)


def sf14_first_count(target, est, names):
    """SF14: "correct" read on the first count rather than the confirmed count gives another set; CP-THN-04 s.5
    (the confirmed count is posted as the location's record) with SCS-07 4.2 rules it out."""
    faces, c = E.prepared(target)
    c["hit"] = c.first_count_qty.astype(int) == c.system_qty.astype(int)
    r = E.rung3(faces, c)
    first_set = sorted(names[k] for k, v in r.items() if v[E.GOLDEN_KEY] >= W.LINE)
    ok(first_set == ["Bellshill", "Daventry", "Hinckley", "Magor"],
       "SF14: the first-count reading gives Bellshill, Daventry, Hinckley and Magor (%s), not the six" % first_set)
    prog = [f for f in os.listdir(target) if f.startswith("Corderoy_CP-THN-04") and f.endswith(".docx")]
    ok(len(prog) == 1, "SF14: the count programme ships as one docx")
    txt = re.sub(r"\s+", " ", _docx_text(os.path.join(target, prog[0])))
    ok("The confirmed count (the recount where there is one, otherwise the first count) is posted as the location's record"
       in txt, "SF14: CP-THN-04 s.5 in the shipped docx posts the confirmed count as the record")
    ok("equals the quantity a count under the 3PL's count programme would record" in " ".join(t for _, t in DC.STANDARD),
       "SF14: SCS-07 4.2 defines correct against what a count under the programme records")


def _whole(est):
    return {n: round(est[n][E.GOLDEN_KEY]) for n in W.NAMES}


def _whole_from(r3):
    names = {c["code"]: c["name"] for c in W.CENTRES}
    return {names[k]: round(v[E.GOLDEN_KEY]) for k, v in r3.items()}


def _golden_with(target, extra):
    loc, _ = E.load(target)
    faces, c = E.prepared(target, include_out_of_scope=True)
    ins = E.in_scope(loc)[["site", "location"]]
    keep = pd.concat([ins, extra]).drop_duplicates()
    f = faces.merge(keep, on=["site", "location"])
    cc = c.merge(keep, on=["site", "location"])
    return _whole_from(E.rung3(f, cc))


def invariance(target, est):
    faces, c = E.prepared(target, utc_days=True)
    ok(_whole_from(E.rung3(faces, c)) == _whole(est), "closure: UTC calendar days against UK trading days move no whole per cent")
    allf, allc = E.prepared(target, include_out_of_scope=True)
    loc, _ = E.load(target)
    r = E.rung3(E.in_scope(loc), allc.merge(E.in_scope(loc)[["site", "location"]], on=["site", "location"]))
    ok(_whole_from(r) == _whole(est), "closure: the estimate reads only in-scope faces' counts")
    cnt = pd.read_csv(os.path.join(target, S.FILES["counts"]), dtype=str, keep_default_na=False)
    ins = E.in_scope(loc)
    lc = cnt.merge(ins[["site", "location", "slot_class"]], on=["site", "location"])
    first = lc.groupby(["site", "location"]).counted_utc.min()
    ok(len(first) == len(ins), "closure 12: every in-scope face has a count in the export")
    days = E.trading_day(lc.counted_utc)
    gaps = lc.assign(day=days).sort_values(["site", "location", "counted_utc"]).groupby(["site", "location"]).day.apply(
        lambda s: s.diff().max() if len(s) > 1 else 0)
    ok(gaps.max() <= 91 + 7, "closure 12: no in-scope face goes longer than its cycle plus roll-over without a count")
    reasons = set(cnt.reason_code)
    ok(reasons == {"CYC", "SHP", "NEG", "EMP", "OVR"}, "closure 19: reason codes are the programme's five")
    rows = len(cnt)
    ok(len(cnt.count_task.unique()) == rows, "closure 15: one row per count task")


def clean_data_and_lens(target, est):
    # the main call reads two files; every ask device sits elsewhere
    tmp = tempfile.mkdtemp()
    for k in ("counts", "locations"):
        shutil.copy(os.path.join(target, S.FILES[k]), os.path.join(tmp, S.FILES[k]))
    e2 = E.everything(tmp)
    shutil.rmtree(tmp)
    ok(all(abs(e2[n][E.GOLDEN_KEY] - est[n][E.GOLDEN_KEY]) < 1e-9 for n in W.NAMES),
       "clean-data test: the answer recomputes from the count history and location master alone (every ask device repaired or removed)")
    ok(qual(e2, "rung0_all_counts") != qual(e2, E.GOLDEN_KEY), "clean-data test: the naive answer and the answer still differ")
    ok(set(qual(est, "rung2_class_weighted")) != set(GOLD), "lens swap: the count rate and the state at 06:00 are different moments and different sets")
    cols_c = set(pd.read_csv(os.path.join(target, S.FILES["counts"]), nrows=1).columns)
    cols_l = set(pd.read_csv(os.path.join(target, S.FILES["locations"]), nrows=1).columns)
    for bad in ("batch_no", "best_before", "cost_per_case", "depot", "store_no", "age", "days_since", "last_counted"):
        ok(bad not in cols_c | cols_l, "separation: no %s column inside the main population" % bad)


def bins_and_subsets(target, world):
    out = {}
    ga = A.ask_a(target)
    gb = A.ask_b(target)
    out["a"], out["b"] = ga, gb
    for n in W.NAMES:
        ok(abs(B.bin_offset(ga[n], 1000)) <= 300, "%s: ask A at least 200 from its £1,000 edge (%.0f)" % (n, ga[n]))
        ok(abs(B.bin_offset(gb[n], 100)) <= 30, "%s: ask B at least 20 from its 100-case edge (%.1f)" % (n, gb[n]))
    # ask A: every subset of mishandlings outside the bin on every centre
    flags = ["fanout", "units", "case_version", "p10"]
    for r in range(1, 5):
        for sub in itertools.combinations(flags, r):
            kw = dict(fanout="fanout" not in sub, units="units" not in sub,
                      case_version="first" if "case_version" in sub else "current", p10="p10" not in sub)
            x = A.ask_a(target, **kw)
            for n in W.NAMES:
                ok(round(x[n], -3) != round(ga[n], -3) and abs(x[n] - ga[n]) >= 1000,
                   "ask A, %s mishandled: %s outside the bin" % ("+".join(sub), n))
    x = A.ask_a(target, overclean=True)
    for n in W.NAMES:
        ok(abs(x[n] - ga[n]) >= 1000 and x[n] < ga[n], "ask A over-cleaned (one row per line per centre): %s low, outside the bin" % n)
    stops_a = {"1 lazy": A.ask_a(target, fanout=False, units=False, p10=False),
               "2 fan-out handled": A.ask_a(target, units=False, p10=False),
               "3 period 10 missed": A.ask_a(target, p10=False),
               "4 over-cleaned": A.ask_a(target, overclean=True), "5 golden": ga}
    for n in W.NAMES:
        ok(abs(stops_a["1 lazy"][n] - ga[n]) >= 2000, "ask A lazy delta at least two bins: %s" % n)
        ok(len({round(s[n], -3) for s in stops_a.values()}) == 5, "ask A stops distinct: %s" % n)
    # ask B: every combination of basis, units and closures
    for basis in ("run", "start", "daily"):
        for units in (True, False):
            for closures in (True, False):
                if (basis, units, closures) == ("daily", True, True):
                    continue
                x = A.ask_b(target, basis=basis, units=units, closures=closures)
                for n in W.NAMES:
                    ok(round(x[n], -2) != round(gb[n], -2) and abs(x[n] - gb[n]) >= 100,
                       "ask B, basis %s units %s closures %s: %s outside the bin" % (basis, units, closures, n))
    x = A.ask_b(target, overclean=True)
    for n in W.NAMES:
        ok(abs(x[n] - gb[n]) >= 100 and x[n] < gb[n], "ask B over-cleaned (re-zoned stores dropped): %s low, outside the bin" % n)
    stops_b = {"1 lazy": A.ask_b(target, basis="run", units=False, closures=False),
               "2 start map": A.ask_b(target, basis="start"), "3 Boxing Day missed": A.ask_b(target, closures=False),
               "4 over-cleaned": A.ask_b(target, overclean=True), "5 golden": gb}
    for n in W.NAMES:
        ok(abs(stops_b["1 lazy"][n] - gb[n]) >= 200, "ask B lazy delta at least two bins: %s" % n)
        ok(len({round(s[n], -2) for s in stops_b.values()}) == 5, "ask B stops distinct: %s" % n)
    # the chart
    order = sorted(W.NAMES, key=lambda n: -gb[n])
    ok(order[0] == "Hinckley", "chart title on the golden path names Hinckley")
    run = A.ask_b(target, basis="run")
    ok(max(run, key=run.get) == "Thurrock", "chart title on the run's depots names Thurrock")
    ok(sorted(W.NAMES, key=lambda n: -run[n]) != order, "chart order on the run's depots differs")
    for n in W.NAMES:
        ok(abs(gb[n] - gb[order[0]]) > 0 or n == order[0], "chart: no tie for the largest")
    out["order"] = order
    out["stops_a"], out["stops_b"] = stops_a, stops_b
    return out


def cracker_and_pair(target, asks):
    ga, gb = asks["a"], asks["b"]
    crack_a = A.ask_a(target, fanout=False, units=True, p10=False)
    for n in W.NAMES:
        ok(round(crack_a[n], -3) != round(ga[n], -3), "cracker sheet, ask A misses: %s" % n)
    crack_b = A.ask_b(target, basis="run", units=True, closures=True)
    for n in W.NAMES:
        ok(round(crack_b[n], -2) != round(gb[n], -2), "cracker sheet, ask B misses: %s" % n)
    ok(sorted(W.NAMES, key=lambda n: -crack_b[n]) != asks["order"], "cracker sheet, chart order misses")
    ok(max(crack_b, key=crack_b.get) != asks["order"][0], "cracker sheet, chart title misses")
    # mirror sheet: the best response that misses the call runs the same ask path
    crit_ask = 8 + 8 + 4
    kept = 1  # one bar per centre, structural
    L = kept / crit_ask
    C = 38 + 7 + 55 * L
    Sx = 5 + 7 + 55 * L
    ceiling = math.ceil((C + Sx) / 2)
    ok(ceiling <= 40, "pair ceiling at 40 or under (%d)" % ceiling)
    return dict(C=C, S=Sx, ceiling=ceiling, crack_a=crack_a, crack_b=crack_b)


def input_gates(target, meta_path):
    files = sorted(os.listdir(target))
    ok(len(files) >= 10, "input gate: 10 or more files (%d)" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok(len(fmts) >= 3, "input gate: 3 or more formats (%s)" % sorted(fmts))
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    ok(big >= 25000, "input gate: a file of 25,000 or more rows (%d)" % big)
    meta = json.load(open(meta_path))
    ok(len(meta["distractor_files"]) >= 2 and all(f in files for f in meta["distractor_files"]),
       "input gate: two distractors named in metadata.json")
    for f in files:
        ok("distractor" not in f.lower(), "no file name says distractor: %s" % f)
    # distractors unused: the golden recomputes with both removed
    tmp = tempfile.mkdtemp()
    for f in files:
        if f not in meta["distractor_files"]:
            shutil.copy(os.path.join(target, f), os.path.join(tmp, f))
    e = E.everything(tmp)
    a, b = A.ask_a(tmp), A.ask_b(tmp)
    shutil.rmtree(tmp)
    ok(qual(e, E.GOLDEN_KEY) == GOLD, "distractors unused: the call recomputes without them")
    ok(a == A.ask_a(target) and b == A.ask_b(target), "distractors unused: both asks recompute without them")
    ok(len(meta["deliverables"]) == 1, "one deliverable")


def realism(target, world):
    cnt = pd.read_csv(os.path.join(target, S.FILES["counts"]), dtype=str, keep_default_na=False)
    by = cnt.groupby("site").size()
    ok(by.nunique() == len(by), "realism: no two centres carry the same number of count rows")
    m = cnt.assign(month=cnt.counted_utc.str[:7]).groupby(["site", "month"]).size()
    ok(m.groupby(level=0).nunique().min() >= 5, "realism: monthly count volumes vary at every centre")
    loc, _ = E.load(target)
    ins = E.in_scope(loc).groupby("site").size()
    ok(ins.nunique() == len(ins) and all(v % 100 for v in ins), "realism: in-scope face counts differ and none is round")
    fc = pd.read_csv(os.path.join(target, A.FILES["forecast"]), dtype=str)
    fc["q"] = fc.fcst_qty.astype(float)
    nun = fc.groupby(["store_no", "category"]).q.nunique()
    ok(nun.min() >= 10, "realism: no store's category forecast is a constant stream")
    rows = {f: (sum(1 for _ in open(os.path.join(target, f))) if f.endswith(".csv") else None) for f in os.listdir(target)}
    vals = [v for v in rows.values() if v]
    ok(len(set(vals)) == len(vals), "realism: no two CSVs carry the same row count")
    ok(all(v % 1000 for v in vals), "realism: no CSV row count is a round thousand")
    # people: only the card's drawn personas appear in the documents
    card = json.load(open(os.path.join(B.REPO, ".claude", "skills", "fingerprint", "cards", "task229.json")))
    people = set(card["world"]["people"])
    text = " ".join(t for _, t in DC.STANDARD) + " " + " ".join(t if isinstance(t, str) else "" for _, t in DC.PROGRAMME)
    text += open(os.path.join(target, DC.FILES["notes"])).read()
    for p in ("Arthur Mason", "Leonard Finch"):
        ok(p in people and (p in text), "realism: persona %s drawn and on the card" % p)
    # containers scrubbed
    r = subprocess.run([sys.executable, B.SCRUB, target, "--floor", "2022-01-01", "--ceiling", "2026-12-07"],
                       capture_output=True, text=True)
    sig = [l for l in r.stdout.splitlines() if any(s in l for s in ("python-docx", "openpyxl", "reportlab", "ReportLab"))]
    ok(not sig, "realism: no container carries its writer's signature")
    # dates coherent with the setting: nothing posted after the pull
    ok(cnt.posted_utc.max() < "2026-12-07T06:00:00Z", "realism: no count posted after the stand-down")
    snap = pd.read_csv(os.path.join(target, A.FILES["batches"]), dtype=str)
    ok(snap.received_utc.max() < "2026-12-07T06:00:00Z", "realism: no batch received after the snapshot")
    cal = pd.read_csv(os.path.join(target, A.FILES["calendar"]), dtype=str)
    ok(cal.updated_utc.max() < "2026-12-07", "realism: the calendar's last update precedes the pull")
    ok(set(card["world"]["people"]) >= {"Rhys Flynn", "Stacey Sykes", "Arthur Mason", "Leonard Finch"}, "realism: card lists the four personas")


def run(target, world, meta_path):
    del LOG[:]
    est = main_path(target, world)
    semantic_forks(target, world, est)
    invariance(target, est)
    clean_data_and_lens(target, est)
    asks = bins_and_subsets(target, world)
    pair = cracker_and_pair(target, asks)
    input_gates(target, meta_path)
    realism(target, world)
    return len(LOG), dict(est=est, asks=asks, pair=pair)
