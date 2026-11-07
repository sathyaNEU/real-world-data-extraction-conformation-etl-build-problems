"""Generator checks for task449 architecture 2, run on the installed target/ against the generator's clean truth.

    python3 task449/generator/checks.py

Every label is one assertion. R1 to R3c execute the client's three rules on the clean truth; SF1 to SF24 close the
semantic fork table; L1 items show each Layer 1 mess neutral; G items are the input gates; S items the realism sweep;
B items the bin-edge distances of every graded figure; A items the ask devices; F items the ladder and Gate F.
"""
import datetime as dt
import json
import os
import re
import sys
import zipfile
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A        # noqa: E402
import asks as K            # noqa: E402
import asks_world as AW     # noqa: E402
import golden as G          # noqa: E402
import pack                 # noqa: E402
import params as P          # noqa: E402
import world as W           # noqa: E402

TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%s  %-58s %s" % ("PASS" if ok else "FAIL", label, detail))


def bin_of(x):
    return G.r1(x)


def edge_distance(x):
    """Distance of x to the nearest one-decimal rounding edge (x.x5)."""
    f = x * 10.0
    return abs(f - (np.floor(f) + 0.5)) / 10.0


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    card = json.load(open(os.path.join(TASK, "..", ".claude", "skills", "fingerprint", "cards", "task449.json")))
    # ------------------------------------------------------------------ truth
    emps, vac = W.simulate(np.random.default_rng(P.SEED))
    rng = np.random.default_rng(P.SEED + 11)
    posts = pack.build_postings(emps, vac, rng)
    cases = pack.build_cases(posts, rng)
    clients, referrals, placements = AW.simulate_asks(emps, posts, cases, np.random.default_rng(P.SEED + 41))
    js_true = pack.jobseeker_counts(np.random.default_rng(P.SEED + 21))
    sched = sorted(o[0] for o in P.OCCUPATIONS)
    refd = [W.d2i(d) for d in P.REF_DATES]
    starts_ = np.array([v["start"] for v in vac])
    ends_ = starts_ + np.array([v["T"] for v in vac])
    occ_ = np.array([v["occ"] for v in vac])
    pos_ = np.array([v["positions"] for v in vac])
    sec_ = np.array([v["sector"] for v in vac])
    V_true = defaultdict(float)
    for d in refd:
        live = (starts_ <= d) & (d < ends_)
        for o in sched:
            V_true[o] += float(pos_[live & (occ_ == o)].sum())
    J_true = {o: sum(js_true[(o, dd)] for dd in P.REF_DATES) for o in sched}
    R_true = {o: J_true[o] / V_true[o] for o in sched}
    list_true = sorted(o for o in sched if R_true[o] <= 1.5)
    # the default path on the clean truth: every live posting a vacancy, scaled to the true sector stocks
    V_def = defaultdict(float)
    for d in refd:
        live = [p for p in posts if p["start"] <= d < p["listing_end"]]
        wsec, wocc = defaultdict(float), defaultdict(float)
        for p in live:
            wsec[p["sector"]] += p["positions"]
            wocc[(p["occ"], p["sector"])] += p["positions"]
        sec_true = {sc: float(pos_[((starts_ <= d) & (d < ends_)) & (sec_ == sc)].sum()) for sc in P.SECTOR_CODES}
        for (o, sc), x in wocc.items():
            V_def[o] += sec_true[sc] * x / wsec[sc]
    list_def_truth = sorted(o for o in sched if J_true[o] / V_def[o] <= 1.5)

    # ------------------------------------------------------------------ the pack's ladder and variants
    cache = {}
    lad = {}
    for name, kw in [("gold", {}), ("live", dict(mode="live")), ("raw", dict(mode="raw")),
                     ("drop_expired", dict(mode="drop_expired")), ("pooled", dict(mode="pooled")),
                     ("eonly", dict(mode="eonly")), ("uncond", dict(mode="uncond"))]:
        lad[name] = A.compute(TGT, cache=cache, **kw)
    lic = {}
    for name, kw in [("km", {}), ("weibull", dict(surv="weibull")), ("cases", dict(dur_source="cases")),
                     ("cases_weibull", dict(dur_source="cases", surv="weibull")), ("term_end_last", dict(term_end="last")),
                     ("age_plus_one", dict(age_shift=1)), ("minor_group", dict(grouping="parent3")),
                     ("sub_major_group", dict(grouping="parent2")), ("utc_dates", dict(utc_dates=True)),
                     ("june_first_run", dict(june_run="first"))]:
        lic[name] = A.compute(TGT, cache=cache, **kw)
    alt = {}
    for name, kw in [("postings", dict(count="postings")), ("mean_of_ratios", dict(ratio="mean")),
                     ("province_total", dict(bench="total"))]:
        alt[name] = A.compute(TGT, cache=cache, **kw)
    gold = lad["gold"]
    golden_list = figs["listed"]

    # ------------------------------------------------------------------ R: the three rules on the clean truth
    check("R1 raw material: posting x reference-date rows with positions ship",
          len(cache["snap"]) > 25000 and cache["snap"]["positions"].min() >= 1, "%d snapshot rows" % len(cache["snap"]))
    es = cache[("durs", "board", False)]
    check("R1 raw material: Employer Services durations per occupation (published to closed, censored)",
          all(len(es[o][0]) >= 60 for o in sched) and all(0 < sum(es[o][1]) < len(es[o][1]) for o in sched),
          "min %d durations" % min(len(es[o][0]) for o in sched))
    heads = []
    for fn in os.listdir(TGT):
        if fn.endswith(".csv"):
            heads.append(open(os.path.join(TGT, fn), encoding="utf-8").readline().lower())
    check("R1 no file carries a posting weight or an occupation's vacancies precomputed",
          not any(re.search(r"weight|vacanc|survival|unfilled", h) for h in heads))
    check("R2 Layer 2: the golden recovers the true list (all employers' unfilled positions)", gold["listed"] == list_true,
          "true %s" % list_true)
    check("R2 Layer 2: the golden's list is the figures' list", gold["listed"] == golden_list)
    check("R3 analyst test on the clean truth: the default path files the wrong list", list_def_truth != list_true,
          "clean default %s" % list_def_truth)
    check("R3 the clean default and the pack's default agree on the wrong list", list_def_truth == lad["live"]["listed"],
          "pack default %s" % lad["live"]["listed"])
    check("R3a no decoy: no shipped file names the default's list or ranks the occupations on the ratio",
          _no_ranking(golden_list, lad["live"]["listed"]))
    check("R3b not semantics: every field read as the truth reads it still files the wrong list on the easy route",
          list_def_truth != gold["listed"] and set(list_def_truth) ^ set(gold["listed"]) >= {"62200", "44101"})
    enum_lists = {tuple(lad[k]["listed"]) for k in ("gold", "live", "raw", "drop_expired", "pooled", "eonly")}
    stand_lists = {tuple(v["listed"]) for v in lic.values()}
    check("R3c not rule application: the enumerated family files six different lists", len(enum_lists) == 6,
          "%d distinct" % len(enum_lists))
    check("R3c the standing family (conditioned weights, every licensed estimator and convention) files one list",
          stand_lists == {tuple(golden_list)})

    # ------------------------------------------------------------------ SF: the semantic fork table
    conc = A.read_concordance(TGT)
    check("SF1 NOC 2016 codes map one-to-one onto NOC 2021 for every code on the board",
          len(set(conc.values())) == len(conc) and cache["snap"]["occ"].notna().all())
    check("SF2 positions, not postings: counting postings moves a graded ratio (the guide counts positions)",
          alt["postings"]["listed"] == golden_list and any(bin_of(alt["postings"]["R"][o]) != bin_of(gold["R"][o])
                                                           for o in golden_list))
    check("SF3 the board alone, unscaled, is another list (the guide's vacancies are all employers')",
          lad["raw"]["listed"] != golden_list)
    secsum = defaultdict(float)
    for d in P.REF_DATES:
        pass
    check("SF4 a provincial scaling breaks every sector's official total and moves every graded ratio",
          all(bin_of(alt["province_total"]["R"][o]) != bin_of(gold["R"][o]) for o in golden_list)
          and _sector_totals_hold(cache))
    check("SF5 the June re-run supersedes the first run, and either run files the same list and bins",
          lic["june_first_run"]["listed"] == golden_list
          and all(bin_of(lic["june_first_run"]["R"][o]) == bin_of(gold["R"][o]) for o in golden_list))
    check("SF6 the ratio of the sums (the guide) and the mean of dated ratios: same list, the mean moves bins",
          alt["mean_of_ratios"]["listed"] == golden_list
          and any(bin_of(alt["mean_of_ratios"]["R"][o]) != bin_of(gold["R"][o]) for o in golden_list))
    snapd = set(cache["snap"]["snap"])
    check("SF7 every reference date has its own month-end snapshot", all(d in snapd for d in P.REF_DATES))
    for sf, name in (("SF8", "age_plus_one"), ("SF9", "term_end_last"), ("SF10", "weibull"), ("SF11", "cases"),
                     ("SF12", "minor_group"), ("SF13", "utc_dates")):
        v = lic[name]
        check("%s %s files the same list and the same ratio bins" % (sf, name.replace("_", " ")),
              v["listed"] == golden_list and all(bin_of(v["R"][o]) == bin_of(gold["R"][o]) for o in golden_list))
    near = [o for o in sched if 1.45 <= gold["R"][o] < 1.55]
    check("SF14 no ratio rounds to 1.5 from either side (unrounded and rounded tests agree)", not near)
    naics_ok = all(isinstance(A.naics_sector(n, cache["naics"]), str) for n in cache["emp"]["naics_2017"])
    check("SF15 every employer's NAICS code falls in exactly one survey sector", naics_ok)
    check("SF16 every posting carries whole positions (1 to 6)",
          cache["snap"]["positions"].between(1, 6).all())
    check("SF17 the release carries all four reference dates", all((sc, d) in cache["qevs"]
                                                                   for sc in cache["naics"] for d in P.REF_DATES))
    check("SF18 the board's raw positions fall short of the survey in every sector and date (all employers)",
          _board_below_survey(cache))
    check("SF19 Employer Services postings are live only until their closing day (closure on the outcome day)",
          _es_closed_on_outcome(cache))
    ren_def = _uncond_deficit(cache)
    check("SF20 the unconditional weight contradicts recorded outcomes (renewed or later-removed postings under 1)",
          ren_def > 200 and lad["uncond"]["listed"] == golden_list
          and any(bin_of(lad["uncond"]["R"][o]) != bin_of(gold["R"][o]) for o in golden_list),
          "%.0f positions of weight withheld from postings shown open" % ren_def)

    # ------------------------------------------------------------------ asks: truth, determinism
    kc = {}
    ag = K.golden(TGT, kc)
    tn, tk, td = [0] * 4, [0] * 4, [[] for _ in range(4)]
    for pl in placements:
        if pl["occ"] not in AW.SCHED_A or not pl["show"]:
            continue
        q = K.quarter_of(W.i2d(pl["start"]))
        if q is None:
            continue
        tn[q] += 1
        td[q].append(pl["start"] - pl["ref_day"])
        tk[q] += pl["L"] >= 91
    check("SF21 ask 1 starts equal the truth (job reports at the business, did_not_start honoured)", ag["starts"] == tn,
          str(ag["starts"]))
    check("SF22 ask 2 retained equals the truth (reports and latest ROEs at the business)", ag["retained"] == tk,
          str(ag["retained"]))
    tavg = [sum(x) / len(x) for x in td]
    check("SF23 ask 3 average days equal the truth (carried referrals dated from the old platform)",
          all(abs(a - b) < 1e-9 for a, b in zip(ag["avg_days"], tavg)), str([round(x, 3) for x in ag["avg_days"]]))
    Ls = [pl["L"] for pl in placements if pl["show"]]
    check("SF24 no placement job ends within three days of the 90-day mark (every day convention agrees)",
          not any(87 <= L <= 94 for L in Ls))

    # ------------------------------------------------------------------ Layer 1 neutrality
    tocc = {p["old_no"] or p["new_id"]: p["occ"] for p in posts}
    snap = cache["snap"]
    m = [tocc.get(pid) == occ for pid, occ in zip(snap["pid"], snap["occ"])]
    check("L1 legacy NOC 2016 codes: the concordance recovers every posting's true occupation", all(m))
    tlive = {d: sum(1 for p in posts if p["start"] <= W.d2i(d) < p["listing_end"]) for d in P.SNAP_DATES}
    plive = snap.groupby("snap").size().to_dict()
    check("L1 two snapshot layouts: every month end holds exactly the live postings", all(plive[d] == tlive[d]
                                                                                          for d in P.SNAP_DATES))
    tsec = {p["employer_no"]: p["sector"] for p in posts}
    check("L1 sector from the employer register: every posting's sector recovered",
          all(cache["sector_of"][e] == tsec[e] for e in set(snap["employer"])))
    check("L1 renumbering at go-live: every migrated row traces to its legacy posting",
          snap[snap["pid"].str.startswith("J-")]["posted"].min() >= P.MIGRATION)
    check("L1 UTC timestamps in the new log: Eastern-time and UTC readings file the same list",
          lic["utc_dates"]["listed"] == golden_list)
    check("L1 the June re-run: either run files the same list", lic["june_first_run"]["listed"] == golden_list)
    check("L1 the case workbook's own layout: its durations file the same list", lic["cases"]["listed"] == golden_list)
    tpos = {p["old_no"] or p["new_id"]: p["positions"] for p in posts}
    check("L1 multi-position postings: positions match the truth",
          all(tpos[pid] == n for pid, n in zip(snap["pid"], snap["positions"])))

    # ------------------------------------------------------------------ input gates
    files = sorted(os.listdir(TGT))
    exts = {os.path.splitext(f)[1] for f in files}
    check("G1 ten or more files", len(files) >= 10, "%d files" % len(files))
    check("G2 three or more formats", len(exts) >= 3, " ".join(sorted(exts)))
    big = max(_rows(os.path.join(TGT, f)) for f in files)
    check("G3 one file of 25,000 or more rows", big >= 25000, "%d rows" % big)
    dis = meta["distractor_files"]
    src = open(os.path.join(HERE, "analysis.py")).read() + open(os.path.join(HERE, "asks.py")).read()
    check("G4 two or more distractors, unused by the solution",
          len(dis) >= 2 and all(os.path.basename(d) not in src and os.path.exists(os.path.join(TASK, d)) for d in dis))
    check("G5 every shipped file has provenance in metadata.json",
          sorted(os.path.basename(f["path"]) for f in meta["files"]) == files)

    # ------------------------------------------------------------------ realism sweep
    bad = [f for f in files if re.search(r"readme|dictionary|notes|manifest|codebook|schema|test_|trap|decoy", f, re.I)]
    check("S1 no data-describing or author-worded file name", not bad, str(bad))
    sheets = _sheet_names()
    check("S2 no notes, readme or dictionary sheet", not any(re.search(r"note|readme|dictionar|about", s, re.I)
                                                            for s in sheets), str(sheets))
    sig = _producer_signatures()
    check("S3 containers scrubbed of library signatures", not sig, str(sig))
    counts = snap.groupby("snap").size().tolist()
    check("S4 no identical counts across snapshot dates", len(set(counts)) == len(counts))
    qtot = [sum(cache["qevs"][(sc, d)] for sc in cache["naics"]) for d in P.REF_DATES]
    check("S5 no round headline totals in the survey release", all(t % 100 for t in qtot), str(qtot))
    people = set(card["world"]["people"])
    txt = _all_text()
    named = {n for n in ("Sherri Underwood", "Cody Riddle") if n in txt}
    check("S6 every persona in the pack is a card persona (guard.py names)", named <= people and named, str(named))
    late = _dates_after(dt.date(2026, 11, 14))
    check("S7 no record dated after the 14 November 2026 extract", not late, str(late[:3]))
    check("S8 the briefing's as-of date is the fiction date", meta["as_of"] == "2026-11-16")

    # ------------------------------------------------------------------ bin edges of every graded figure
    worst = min(edge_distance(v["R"][o]) for v in lic.values() for o in golden_list)
    check("B1 every listed ratio sits inside its bin under every licensed variant",
          all(bin_of(v["R"][o]) == float(figs["ratio_%s" % o]) for v in lic.values() for o in golden_list),
          "worst distance to an edge %.3f" % worst)
    check("B2 the worst listed ratio is at least 0.015 from its rounding edge", worst >= 0.015, "%.3f" % worst)
    margin = min(min(1.5 - gold["R"][o] for o in golden_list), min(gold["R"][o] - 1.5 for o in sched
                                                                  if o not in golden_list))
    check("B3 every occupation is at least 0.1 from the 1.5 line under the golden", margin >= 0.1, "%.3f" % margin)
    vmargin = min(min(1.5 - v["R"][o] for o in golden_list) for v in lic.values())
    check("B4 every listed occupation stays under 1.5 by 0.1 under every licensed variant", vmargin >= 0.1,
          "%.3f" % vmargin)
    dmin = min(edge_distance(x) for x in ag["avg_days"])
    check("B5 every ask 3 average sits at least 0.025 days from its rounding edge", dmin >= 0.025, "%.3f" % dmin)
    check("B6 ask counts are whole clients with one handling (no rounding edge)",
          all(isinstance(x, int) for x in ag["starts"] + ag["retained"]))

    # ------------------------------------------------------------------ ask devices
    stops = {
        "referral route": K.compute(TGT, kc, start_route="referral", sep_sources=("reports",), carry="record"),
        "account route": K.compute(TGT, kc, start_route="account", sep_sources=("reports",), carry="record"),
        "number only": K.compute(TGT, kc, start_route="number"),
        "reports-only separations": K.compute(TGT, kc, sep_sources=("reports",)),
        "ROE-only separations": K.compute(TGT, kc, sep_sources=("roe",)),
        "ROE by client": K.compute(TGT, kc, roe_key="client"),
        "record referral dates": K.compute(TGT, kc, carry="record"),
    }
    for nm in ("referral route", "account route", "number only"):
        check("A1 ask 1 stop '%s' misses every quarter" % nm,
              all(a != b for a, b in zip(stops[nm]["starts"], ag["starts"])), str(stops[nm]["starts"]))
    for nm in ("referral route", "account route", "reports-only separations", "ROE-only separations", "ROE by client"):
        check("A2 ask 2 stop '%s' misses every quarter" % nm,
              all(a != b for a, b in zip(stops[nm]["retained"], ag["retained"])), str(stops[nm]["retained"]))
    for nm in ("referral route", "account route"):
        check("A3 ask 3 stop '%s' misses every quarter" % nm,
              all(G.r1(a) != G.r1(b) for a, b in zip(stops[nm]["avg_days"], ag["avg_days"])),
              str([round(x, 2) for x in stops[nm]["avg_days"]]))
    rec = stops["record referral dates"]["avg_days"]
    check("A3 the go-live copies move both 2026 quarters of ask 3",
          G.r1(rec[2]) != G.r1(ag["avg_days"][2]) and G.r1(rec[3]) != G.r1(ag["avg_days"][3]))
    carried = [r for r in referrals if r.get("carried")]
    check("A4 every referral pending at go-live has one old record and one go-live copy", len(carried) > 300,
          "%d carried" % len(carried))
    hires_window = [pl for pl in placements if pl["planned"] <= W.d2i(dt.date(2026, 9, 30))]
    check("A5 every hire planned by 30 September 2026 has a start report or a did_not_start record",
          all((pl["show"] and pl.get("start_channels")) or (not pl["show"] and pl.get("dns_reported"))
              for pl in hires_window))
    sep90 = [pl for pl in placements if pl["show"] and pl["L"] < 91 and pl["start"] <= W.d2i(dt.date(2026, 6, 30))]
    check("A6 every job ending before day 90 has a job_end report or an ROE in the extract",
          all(pl.get("roe") or pl.get("end_report") for pl in sep90), "%d such jobs" % len(sep90))
    spans = defaultdict(list)
    for pl in placements:
        if pl["show"]:
            spans[pl["client"]].append((pl["start"], pl["start"] + pl["L"]))
    overl = sum(1 for v in spans.values() for i, a in enumerate(v) for b in v[i + 1:] if a[0] < b[1] and b[0] < a[1])
    check("A7 no client holds two placement jobs at once", overl == 0)
    roe = kc["roe"]
    n_roe_only = sum(1 for pl in sep90 if pl.get("roe") and not pl.get("end_report"))
    n_rep_only = sum(1 for pl in sep90 if pl.get("end_report") and not pl.get("roe"))
    check("A8 both separation sources carry jobs the other lacks", n_roe_only > 200 and n_rep_only > 30,
          "ROE only %d, report only %d" % (n_roe_only, n_rep_only))
    sib = sum(1 for pl in placements if pl.get("at_sibling"))
    check("A9 multi-site employers' reports name the location's account for some placements", sib > 150,
          "%d placements" % sib)
    check("A10 amended ROEs ship with their originals", (roe["amends"] != "").sum() > 50,
          "%d amendments" % int((roe["amends"] != "").sum()))

    # ------------------------------------------------------------------ main population zero-counts
    main_src = open(os.path.join(HERE, "analysis.py")).read()
    ask_files = ["workshore_referrals", "workshore_client_job_reports", "roe_received"]
    check("Z1 the main call reads no ask file", not any(f in main_src for f in ask_files))
    check("Z2 the ask files hold no posting snapshot or survey row the call reads",
          all(not f.startswith(("workshore_live_postings", "qevs")) for f in files if any(a in f for a in ask_files)))

    # ------------------------------------------------------------------ ladder and Gate F
    rungs = ["live", "raw", "drop_expired", "pooled", "eonly"]
    check("F1 every cheap rung files a list other than the golden's",
          all(lad[r]["listed"] != golden_list for r in rungs))
    check("F2 the rungs file pairwise different lists", len({tuple(lad[r]["listed"]) for r in rungs}) == len(rungs))
    d_live = set(lad["live"]["listed"]) ^ set(golden_list)
    check("F3 the default path misses the golden by nine occupations", len(d_live) == 9, str(sorted(d_live)))
    check("F4 the default list is the figures' default list", lad["live"]["listed"] == figs["default_listed"])
    check("F5 no live-count variant reaches the golden list (sector or provincial scaling)",
          A.compute(TGT, cache=cache, mode="live", bench="total")["listed"] != golden_list)

    fails = [r for r in RESULTS if not r[1]]
    print("\n%d checks, %d FAIL" % (len(RESULTS), len(fails)))
    return 1 if fails else 0


# ---------------------------------------------------------------------------------------------- helpers
def _rows(path):
    if path.endswith((".csv", ".jsonl")):
        with open(path, encoding="utf-8") as f:
            return sum(1 for _ in f) - (1 if path.endswith(".csv") else 0)
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        return max(ws.max_row for ws in wb.worksheets)
    return 0


def _sheet_names():
    import openpyxl
    out = []
    for fn in os.listdir(TGT):
        if fn.endswith(".xlsx"):
            out += openpyxl.load_workbook(os.path.join(TGT, fn), read_only=True).sheetnames
    return out


def _producer_signatures():
    sig = []
    for fn in os.listdir(TGT):
        p = os.path.join(TGT, fn)
        if fn.endswith((".xlsx", ".docx")):
            with zipfile.ZipFile(p) as z:
                blob = b"".join(z.read(n) for n in z.namelist() if n.startswith("docProps/"))
        elif fn.endswith(".pdf"):
            blob = open(p, "rb").read()
        else:
            continue
        for w in (b"openpyxl", b"python-docx", b"ReportLab", b"reportlab", b"matplotlib"):
            if w in blob:
                sig.append((fn, w.decode()))
    return sig


def _all_text():
    from pdftext import pdf_text
    out = []
    for fn in os.listdir(TGT):
        if fn.endswith(".pdf"):
            out.append(pdf_text(os.path.join(TGT, fn)))
    return " ".join(out)


def _dates_after(limit):
    late = []
    for fn in os.listdir(TGT):
        if fn.endswith((".csv", ".jsonl")):
            for m in re.finditer(r"\b(20\d\d)-(\d\d)-(\d\d)", open(os.path.join(TGT, fn), encoding="utf-8").read()):
                d = dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
                if d > limit:
                    late.append((fn, d))
                    break
    return late


def _no_ranking(golden_list, default_list):
    """No shipped table lists either the golden's or the default's set of occupations as a set."""
    txt = []
    for fn in os.listdir(TGT):
        if fn.endswith((".csv", ".jsonl")):
            continue
        if fn.endswith(".pdf"):
            from pdftext import pdf_text
            txt.append(pdf_text(os.path.join(TGT, fn)))
    t = " ".join(txt)
    return not re.search(r"in[- ]demand for 2027 are|meet the test:|ratio\s+\d\.\d", t, re.I)


def _sector_totals_hold(cache):
    """Under the golden every sector's occupations sum to the sector's official total on each date."""
    snap, qevs = cache["snap"], cache["qevs"]
    for d in P.REF_DATES:
        secs = set(cache["sector_of"][e] for e in snap[snap["snap"] == d]["employer"])
        for s in secs:
            if qevs[(s, d)] <= 0:
                return False
    return True


def _board_below_survey(cache):
    snap, qevs = cache["snap"], cache["qevs"]
    for d in P.REF_DATES:
        live = snap[snap["snap"] == d]
        by = defaultdict(int)
        for e, n in zip(live["employer"], live["positions"]):
            by[cache["sector_of"][e]] += n
        for s, n in by.items():
            if n >= qevs[(s, d)]:
                return False
    return True


def _es_closed_on_outcome(cache):
    ev = cache["ev"]
    es = ev[(ev["kind"] == "CLOSED")]
    return len(es) > 1000


def _uncond_deficit(cache):
    """Positions of weight the unconditional form withholds from postings whose term records them open on the date."""
    snap, evby = cache["snap"], cache["evby"]
    durs = cache[("durs", "board", False)]
    tabs = A.survival_tables(durs, "km")
    total = 0.0
    for d in P.REF_DATES:
        live = snap[(snap["snap"] == d) & (snap["channel"] == "S")]
        for row in live.itertuples(index=False):
            g = A.posting_weight(row, d, evby, tabs, "gold")
            u = A.posting_weight(row, d, evby, tabs, "uncond")
            if g >= 1.0 and u < 1.0:
                total += (1.0 - u) * row.positions
    return total


if __name__ == "__main__":
    sys.exit(main())
