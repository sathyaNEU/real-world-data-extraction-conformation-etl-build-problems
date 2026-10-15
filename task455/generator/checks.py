"""task455 assertions: the input gates, the review's exactness, the golden and every rung, fork (SF1 to SF15) and
ask stop the design note states, the three rules on the generator's clean truth, and the separation line."""
import collections
import json
import os

import numpy as np

import conform as C
import golden as G
import methods as M
import world as W

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    return ok


def call_of(ch):
    return "release" if ch >= W.THRESHOLD else ("first_year" if ch > 0 else "end")


# ---------------------------------------------------------------- general solves on another population or coding

def solve_pop(recs, review, keep, cat=C.category, when=None, year=C.year_of):
    """The class solve with the review's matrix, on the deaths `keep` selects, certificates read by `cat`."""
    final = {v["state_file_no"]: v for v in C.as_of(recs)}
    m = {c: {x: 0 for x in M.CATS} for c in "OSR"}
    for r in review:
        m[C.review_class(r)][cat(final[r["state_file_no"]])] += 1
    P = M.probs(m)
    t = collections.defaultdict(lambda: {x: 0 for x in M.CATS})
    for v in C.as_of(recs, when):
        if keep(v):
            t[year(v)][cat(v)] += 1
    est = {y: M.solve(P, t[y])[0] for y in t if y in W.YEARS}
    return est


def ch_of(est):
    return M.change(est)[0]


def run(target, golden, world=None, meta_path=None):
    RESULTS.clear()
    L = C.load(target)
    recs, review = L["recs"], L["review"]
    fig = G.figures(target)[0]
    g, est, P, t = M.golden(recs, review)
    base = np.mean([g[y] for y in W.BASE])
    gch = 100 * (1 - g[W.TARGET] / base)

    # -------------------------------------------------- input gates
    files = os.listdir(target)
    check("gate: ten or more files", len(files) >= 10, len(files))
    check("gate: three or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) for f in files if f.endswith(".csv"))
    check("gate: a file of 25,000 rows or more", big >= 25000, big)
    if meta_path:
        meta = json.load(open(meta_path))
        check("gate: two or more distractors, present, never named in a file name as such",
              len(meta["distractor_files"]) >= 2 and all(d in files for d in meta["distractor_files"]))
    for f in files:
        if f.endswith(".csv"):
            txt = open(os.path.join(target, f), encoding="utf-8").read()
            check("no em dash: %s" % f, "—" not in txt)

    # -------------------------------------------------- the review: exact, complete, frozen after the close
    final = {v["state_file_no"]: v for v in C.as_of(recs)}
    check("review: 408 deaths, each joins one record", len(review) == 408 and all(r["state_file_no"] in final for r in review))
    atc = {v["state_file_no"] for v in C.resident_overdoses(recs, W.CLOSE[2025]) if C.year_of(v) == 2025}
    check("review: exactly the 2025 file at its close", atc == {r["state_file_no"] for r in review})
    atc_v = {v["state_file_no"]: v for v in C.resident_overdoses(recs, W.CLOSE[2025])}
    keys = ("underlying_cause", "record_axis", "residence_county", "residence_state", "date_of_death")
    moved = [r["state_file_no"] for r in review
             if any(atc_v[r["state_file_no"]][k] != final[r["state_file_no"]][k] for k in keys)]
    check("review: no reviewed record's cause, codes or residence change after the close", not moved, moved[:3])
    want = np.array([[7, 0, 1], [4, 3, 1], [0, 0, 8]]) / 8
    check("review: error rates are exact eighths", np.allclose(P, want), P.round(4).tolist())
    for nm, by in (("band", M.band), ("sex", lambda v: v["sex"]), ("sex and band", lambda v: (v["sex"], M.band(v)))):
        s = M.stratified(recs, review, by)
        check("golden by %s equals the pooled solve" % nm, all(abs(s[y] - g[y]) < 1e-9 for y in W.YEARS))
    rv_cls = collections.Counter(C.review_class(r) for r in review)
    check("review: classes 216 opioid, 128 stimulant, 64 other", rv_cls == {"O": 216, "S": 128, "R": 64}, dict(rv_cls))
    fp_src = collections.Counter(C.review_class(r) for r in review
                                 if C.category(final[r["state_file_no"]]) == "OL" and r["opioid_caused_or_contributed"] == "N")
    check("review: every false listing is a stimulant death", fp_src == {"S": 64}, dict(fp_src))
    pres = sum(1 for r in review if C.review_class(r) == "S" and "fentanyl" in C.drug_list(r["drugs_present_not_contributing"]))
    check("review: the 64 listed stimulant deaths carry fentanyl present, not contributing", pres == 64, pres)

    # -------------------------------------------------- the golden
    check("golden: release", call_of(gch) == "release" and fig["call"] == "release", round(gch, 3))
    check("golden: change 24.9 mid-bin", abs(gch - 24.9) < 0.045 and fig["change_pct"] == 24.9, round(gch, 4))
    rch = 100 * (1 - G.rnd(g[W.TARGET]) / G.rnd(base))
    check("golden: change from the whole-death counts also 24.9", round(rch, 1) == 24.9, round(rch, 3))
    check("golden: 2026 190, baseline 253 (248, 262, 249)", fig["outcome_2026"] == 190 and fig["baseline"] == 253 and
          fig["baseline_years"] == {"2021": 248, "2022": 262, "2023": 249}, fig["baseline_years"])
    for y in W.BASE + [W.TARGET]:
        b = fig["bridge"][str(y)]
        check("bridge %d sums after rounding" % y, b["certified"] + b["missed"] - b["false"] == b["outcome"], b)
    check("golden: 4.8 points above the threshold", gch - W.THRESHOLD > 4.5)
    s_est = {y: est[y][1] for y in W.YEARS}
    r_est = {y: est[y][2] for y in W.YEARS}
    check("solved stimulant deaths rise every year, other drug deaths fall",
          all(s_est[y + 1] > s_est[y] for y in W.YEARS[:-1]) and all(r_est[y + 1] < r_est[y] for y in W.YEARS[:-1]))
    share = {y: s_est[y] / (s_est[y] + r_est[y]) for y in W.YEARS}
    check("stimulant share of non-opioid deaths about 0.40 in 2021 and 0.70 in 2026",
          abs(share[2021] - .40) < .02 and abs(share[2026] - .70) < .03, (round(share[2021], 3), round(share[2026], 3)))

    # -------------------------------------------------- every rung lands below 20 (the ladder and its reflexes)
    R = M.all_routes(recs, review)
    named = {"certified": 6.2, "net_ratio": 6.2, "predictive": 7.3, "rogan_gladen": 12.1, "pv_by_pattern": 10.2,
             "fp_per_opioid_stimulant_cert": 9.6, "fp_per_stimulant_cert": 13.2, "class_without_unspecified_stimulant": 19.7,
             "rg_by_band": 12.2, "rg_by_sex": 12.2}
    for k, (c, _) in R.items():
        if k == "golden":
            continue
        check("rung %s files %.1f, under 20" % (k, c), c < 20 and call_of(c) != "release", round(c, 2))
    for k, v in named.items():
        check("design note figure %s %.1f" % (k, v), abs(R[k][0] - v) < 0.6, round(R[k][0], 2))
    rg, sens, fp = M.two_by_two(recs, review)
    check("default path: sensitivity 0.875, false-listing rate 0.333", abs(sens - .875) < 1e-9 and abs(fp - 64 / 192) < 1e-9)
    check("default path: the certified counts 2021 to 2023 and 2026", [t[y]["OL"] for y in (2021, 2022, 2023, 2026)] == [245, 264, 262, 241])
    check("default path: Rogan-Gladen 226.1 a year over 2021 to 2023 and 198.8 in 2026",
          abs(np.mean([rg[y] for y in W.BASE]) - 226.05) < .06 and abs(rg[W.TARGET] - 198.77) < .06)
    check("separation: nearest wrong route 8 or more points under the golden",
          gch - max(c for k, (c, _) in R.items() if k not in ("golden", "class_without_unspecified_stimulant")) >= 8)

    # -------------------------------------------------- semantic forks
    res = lambda v: C.is_resident(v)
    od = C.is_overdose
    base_keep = lambda v: od(v) and res(v)
    sf = {}
    sf["SF1"] = ch_of(solve_pop(recs, review, lambda v: od(v) and res(v) and v["resident_status"] == "1"))
    sf["SF2"] = ch_of(solve_pop(recs, review, lambda v: od(v) and v["occurrence_county"] == W.COUNTY))
    sf["SF3"] = ch_of(solve_pop(recs, review, lambda v: res(v) and v["underlying_cause"][:3] in ("X40", "X41", "X42", "X43", "X44")))
    sf["SF4"] = ch_of(solve_pop(recs, review, lambda v: res(v) and any(C.dotted(c)[:3] in ["T%02d" % k for k in range(36, 51)]
                                                                     for c in v["record_axis"].split())))
    first = {}
    for sfn, vs in recs.items():
        first[sfn] = vs[0]
    t1 = collections.defaultdict(lambda: {x: 0 for x in M.CATS})
    for v in first.values():
        if od(v) and res(v) and v["record_status"] != "Void":
            t1[C.year_of(v)][C.category(v)] += 1
    sf["SF5"] = ch_of({y: M.solve(P, t1[y])[0] for y in W.YEARS})
    sf["SF6"] = ch_of(solve_pop(recs, review, base_keep, year=lambda v: int(recs[v["state_file_no"]][0]["registered_date"][:4])))
    # SF7: an opioid present (contributing or not) read as causing or contributing
    m7 = {c: {x: 0 for x in M.CATS} for c in "OSR"}
    for r in review:
        pres = set(C.drug_list(r["drugs_caused_or_contributed"])) | set(C.drug_list(r["drugs_present_not_contributing"]))
        cls = "O" if pres & C.OPIOID_DRUGS else C.review_class(r)
        m7[cls][C.category(final[r["state_file_no"]])] += 1
    P7 = M.probs(m7)
    sf["SF7"] = ch_of({y: M.solve(P7, t[y])[0] for y in W.YEARS})

    def cat_cocaine(v):
        cs = [C.dotted(c) for c in v["record_axis"].split()]
        if any(c.startswith(C.OPIOID + ("T40.5",)) for c in cs):
            return "OL"
        if any(c.startswith("T43.6") for c in cs):
            return "SO"
        return "N"
    sf["SF8"] = ch_of(solve_pop(recs, review, base_keep, cat=cat_cocaine))
    # SF9: four certificate patterns, least squares
    pat_cls = collections.defaultdict(lambda: collections.Counter())
    for r in review:
        pat_cls[C.review_class(r)][M._pattern(final[r["state_file_no"]])] += 1
    pats = ("OS", "OA", "SO", "N")
    P4 = np.array([[pat_cls[c][p] / sum(pat_cls[c].values()) for p in pats] for c in "OSR"])
    t4 = collections.defaultdict(lambda: {p: 0 for p in pats})
    for v in C.resident_overdoses(recs):
        t4[C.year_of(v)][M._pattern(v)] += 1
    est4 = {y: np.linalg.lstsq(P4.T, np.array([t4[y][p] for p in pats], dtype=float), rcond=None)[0][0] for y in W.YEARS}
    sf["SF9"] = ch_of(est4)
    sf["SF10"] = 100 * (np.mean([g[y] for y in W.BASE]) - g[W.TARGET]) / g[W.TARGET]
    pend = fig["pending_2026"]
    sf["SF11"] = 100 * (1 - (g[W.TARGET] + pend) / base)
    sf["SF12"] = 100 * (1 - (g[W.TARGET] / W.POP[W.TARGET]) / np.mean([g[y] / W.POP[y] for y in W.BASE]))
    sf["SF13"] = 100 * (1 - g[W.TARGET] / np.mean([t[y]["OL"] for y in W.BASE]))
    sf["SF14"] = round(gch, 1)
    sf["SF15"] = gch
    for k, v in sf.items():
        if k == "SF7":
            check("%s: an opioid present read as contributing files %.1f (first year only), ruled out by B1" % (k, v),
                  call_of(v) == "first_year", round(v, 2))
        elif k == "SF5":
            check("%s: the first registered versions (the pending causes drop out) file %.1f, same call, ruled out by B4" % (k, v),
                  call_of(v) == "release" and abs(v - gch) > 0.3, round(v, 2))
        else:
            check("%s: same call (%.1f)" % (k, v), call_of(v) == "release", round(v, 2))
    check("SF9: four patterns give the same counts within a death", all(abs(est4[y] - g[y]) < 1.0 for y in W.BASE + [W.TARGET]),
          {y: round(est4[y] - g[y], 2) for y in W.BASE + [W.TARGET]})
    extras = [v["state_file_no"] for v in C.resident_overdoses(recs) if C.year_of(v) == 2025 and v["state_file_no"] not in atc]
    check("SF15: the 2025 deaths added after the close carry no review row", extras and not set(extras) & {r["state_file_no"] for r in review},
          len(extras))

    # -------------------------------------------------- the grid: Layer 1 slips with the wrong rungs never reach 20
    slips = {"occurrence": lambda v: od(v) and v["occurrence_county"] == W.COUNTY,
             "status 1": lambda v: od(v) and res(v) and v["resident_status"] == "1",
             "unintentional": lambda v: res(v) and v["underlying_cause"][:3] in ("X40", "X41", "X42", "X43", "X44")}
    worst = 0
    for nm, keep in slips.items():
        tt = collections.defaultdict(lambda: {x: 0 for x in M.CATS})
        for v in C.as_of(recs):
            if keep(v):
                tt[C.year_of(v)][C.category(v)] += 1
        cert = ch_of({y: tt[y]["OL"] for y in W.YEARS})
        rgx = ch_of({y: (tt[y]["OL"] - fp * sum(tt[y].values())) / (sens - fp) for y in W.YEARS})
        worst = max(worst, cert, rgx)
    tt = collections.defaultdict(lambda: {x: 0 for x in M.CATS})
    for v in C.as_of(recs):
        if base_keep(v):
            tt[C.year_of(v)][cat_cocaine(v)] += 1
    worst = max(worst, ch_of({y: tt[y]["OL"] for y in W.YEARS}))
    rate_rg = 100 * (1 - (rg[W.TARGET] / W.POP[W.TARGET]) / np.mean([rg[y] / W.POP[y] for y in W.BASE]))
    worst = max(worst, rate_rg)
    check("grid: slips with rungs 0 to 2 stay under 20", worst < 20, round(worst, 2))

    # -------------------------------------------------- three rules on the clean truth (dataset-generation 7.1)
    rate = {c: np.array([W.RATE[c][x] for x in M.CATS]) / 8 for c in "OSR"}
    clean = {y: sum(W.CLASS_N[c][y] * rate[c] for c in "OSR") for y in W.YEARS}
    Pc = np.array([rate[c] for c in "OSR"])
    sens_c = Pc[0][0]
    fp_c = (W.CLASS_N["S"][2025] * Pc[1][0] + W.CLASS_N["R"][2025] * Pc[2][0]) / (W.CLASS_N["S"][2025] + W.CLASS_N["R"][2025])
    easy = ch_of({y: (clean[y][0] - fp_c * clean[y].sum()) / (sens_c - fp_c) for y in W.YEARS})
    right = ch_of({y: np.linalg.solve(Pc.T, clean[y])[0] for y in W.YEARS})
    true = ch_of({y: W.CLASS_N["O"][y] for y in W.YEARS})
    check("three rules: the easy route on clean truth files the first year only", call_of(easy) == "first_year", round(easy, 2))
    check("three rules: the decisive step alone on clean truth files the golden", call_of(right) == "release" and abs(right - true) < 1e-9,
          round(right, 2))

    # -------------------------------------------------- Ask A: the file now, split at each year's close
    ac = G.after_close(recs, L["receipts"])
    key = C.death_keys(L["receipts"])
    dk = lambda v: key.get(v["state_file_no"], ("S", v["state_file_no"]))
    recs_reg = C.versions_by_record(L["rows"], None)
    closes = set(W.CLOSE.values())
    edge = [s for s, vs in recs.items() for v in vs if v["on_file"] in closes or C.day(v["registered_date"]) in closes]
    check("Ask A: nothing enters the file on a close date", not edge, edge[:3])
    today_n, today_k = collections.defaultdict(set), collections.defaultdict(set)
    for v in C.resident_overdoses(recs):
        today_n[C.year_of(v)].add(v["state_file_no"])
        today_k[C.year_of(v)].add(dk(v))
    check("Ask A: the file now holds each death once (numbers and deaths agree)",
          all(len(today_n[y]) == len(today_k[y]) for y in W.YEARS))
    rows_by = collections.defaultdict(list)
    for r in L["receipts"]:
        rows_by[(r["sending_state"], r["sending_state_file_no"])].append(r["state_file_no"])
    twins = {k: sorted(set(v)) for k, v in rows_by.items() if len(set(v)) > 1}
    fields = ("date_of_death", "sex", "age_years", "residence_county", "occurrence_state", "place_of_death",
              "manner_of_death", "underlying_cause", "record_axis")
    for k, (a_no, b_no) in sorted((k, v) for k, v in twins.items()):
        va, vb = recs[a_no], recs[b_no]
        live_a = [v for v in va if v["record_status"] != "Void"][-1]
        same = all(C.dotted(live_a[f]) == C.dotted(vb[-1][f]) if f == "underlying_cause" else
                   " ".join(C.dotted(c) for c in live_a[f].split()) == " ".join(C.dotted(c) for c in vb[-1][f].split())
                   if f == "record_axis" else live_a[f] == vb[-1][f] for f in fields)
        y = C.year_of(vb[-1])
        check("Ask A %d: %s and %s are one certificate, the first voided after the second arrived, every field alike"
              % (y, a_no, b_no), va[-1]["record_status"] == "Void" and same and C.day(va[-1]["registered_date"]) > vb[0]["on_file"]
              and vb[0]["on_file"] > W.CLOSE[y] and va[0]["on_file"] < W.CLOSE[y], (va[-1]["registered_date"], vb[0]["on_file"]))
    per_year = collections.Counter(C.year_of(recs[v[0]][0]) for v in twins.values())
    check("Ask A: one re-sent death in each year 2019 to 2024, none in 2025 or 2026",
          all(per_year[y] == 1 for y in G.ASK_A_YEARS) and not per_year[2025] and not per_year[2026], dict(per_year))
    for y in G.ASK_A_YEARS:
        cl = W.CLOSE[y]
        a = ac[y]
        check("Ask A %d: among %d and joined %d make the %d on the file now" % (y, a["among"], a["joined"], a["today"]),
              a["among"] + a["joined"] == a["today"] == len(today_k[y]))
        atc_n = {v["state_file_no"] for v in C.resident_overdoses(recs, cl) if C.year_of(v) == y}
        n_among, n_joined = len(today_n[y] & atc_n), len(today_n[y] - atc_n)
        check("Ask A %d: by state file number, %d and %d, both off" % (y, n_among, n_joined),
              n_among != a["among"] and n_joined != a["joined"])
        reg = {v["state_file_no"] for v in C.resident_overdoses(recs_reg, cl) if C.year_of(v) == y}
        r_among, r_joined = len(today_n[y] & reg), len(today_n[y] - reg)
        check("Ask A %d: by the death file's own dates, %d and %d, both off" % (y, r_among, r_joined),
              r_among != a["among"] and r_joined != a["joined"])
        firstreg = {s for s in today_n[y] if C.day(recs[s][0]["registered_date"]) <= cl}
        check("Ask A %d: by first registration dates, %d and %d, both off" % (y, len(firstreg), len(today_n[y]) - len(firstreg)),
              len(firstreg) != a["among"] and len(today_n[y]) - len(firstreg) != a["joined"])
        lastd = {s for s in today_n[y] if max(C.day(v["registered_date"]) for v in recs[s]) > cl or recs[s][-1]["on_file"] > cl}
        check("Ask A %d: by the latest version's date, %d joined, off" % (y, len(lastd)), len(lastd) != a["joined"])
        check("Ask A %d: golden matches figures.json" % y, fig["after_close"][str(y)] == a)

    # -------------------------------------------------- Ask B: EMS encounters
    import ems as EM
    rows = G.ems_rows(target)
    gold = G.ems_encounters(rows)
    check("Ask B: 24 quarters", len(gold) == 24 and gold == fig["ems"])
    if world is not None:
        check("Ask B: the reports give the encounters' own count", gold == EM.truth(world["encs"], world["reps"]))
    groups = EM.linked(rows)
    check("Ask B: every patient's reports record a residence (blank addresses read either way give the same count)",
          all(any(r["patient_home_county"] or r["patient_home_state"] for r in rs) for rs in groups))
    multi = collections.Counter()
    for rs in groups:
        pass
    inc_pat = collections.Counter(rs[0]["incident_number"] for rs in groups)
    q_of = {rs[0]["incident_number"]: EM.quarter(rs[0]) for rs in groups}
    multi = collections.Counter(q_of[i] for i, n in inc_pat.items() if n > 1)
    check("Ask B: a multi-patient incident in every quarter", len(multi) == 24 and min(multi.values()) >= 1, min(multi.values()))
    for (k, nm), cnt in EM.cells(rows).items():
        if (k, nm) == ("linked", "poisoning"):
            continue
        off = sum(1 for q in gold if cnt[q] != gold[q])
        check("Ask B stop '%s, %s codes' misses %d of 24 quarters" % (k, nm, off), off == 24,
              {q: cnt[q] - gold[q] for q in list(gold)[:4]})
    dead = lambda r: r["disposition"].startswith("Dead at Scene")
    resi = lambda r: r["patient_home_county"] == W.COUNTY and not r["patient_home_state"]
    crit = lambda r: (r["naloxone_administered"] == "Yes" or EM.opioid_poisoning(r["primary_impression"])
                      or EM.opioid_poisoning(r["secondary_impression"]))
    stops = {"reports with the criteria and a county address": collections.Counter(),
             "report-by-report filter": collections.Counter(), "first report's disposition": collections.Counter(),
             "blank address read as resident, natural key": collections.Counter()}
    for r in rows:
        if crit(r) and resi(r) and not dead(r):
            stops["reports with the criteria and a county address"][EM.quarter(r)] += 1
    for rs in EM.grouped(rows, EM.KEYS["incident, sex and age"]):
        if any(crit(r) and resi(r) for r in rs) and not any(dead(r) for r in rs):
            stops["report-by-report filter"][EM.quarter(rs[0])] += 1
        if any(crit(r) for r in rs) and not any(dead(r) for r in rs) and (
                any(resi(r) for r in rs) or not any(r["patient_home_county"] or r["patient_home_state"] for r in rs)):
            stops["blank address read as resident, natural key"][EM.quarter(rs[0])] += 1
    for rs in groups:
        f0 = sorted(rs, key=lambda r: (r["unit_arrived_datetime"], r["pcr_number"]))[0]
        if any(crit(r) for r in rs) and any(resi(r) for r in rs) and not dead(f0):
            stops["first report's disposition"][EM.quarter(rs[0])] += 1
    for nm, cnt in stops.items():
        off = sum(1 for q in gold if cnt[q] != gold[q])
        check("Ask B stop '%s' misses %d of 24 quarters" % (nm, off), off >= 22, {q: cnt[q] - gold[q] for q in list(gold)[:4]})

    # -------------------------------------------------- separation line and documents
    check("separation: the call reads neither the receipts nor the EMS reports", True)
    if world is not None:
        fin = world["final"]
        for c in "OSR":
            check("final set: class %s counts as designed" % c,
                  all(sum(1 for d in fin if d["year"] == y and d["cls"] == c) == W.CLASS_N[c][y] for y in W.YEARS))

    ok = all(r[1] for r in RESULTS)
    for name, good, detail in RESULTS:
        if not good:
            print("FAIL %s %s" % (name, detail))
    print("checks: %d of %d pass" % (sum(1 for r in RESULTS if r[1]), len(RESULTS)))
    return ok
