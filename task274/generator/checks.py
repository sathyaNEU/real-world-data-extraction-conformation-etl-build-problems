"""task274 generator checks: the assertions the build ships on.

    python3 task274/generator/checks.py

Runs on the generator's clean truth (world, records) and on the cut pack (verify, ceiling). Every semantic
fork row of the design note (SF1 ...) and every client rule (R1, R2, R3) has its own assertion. Exit 0 only
when every assertion holds.
"""
import csv
import datetime as dt
import glob
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)

import world as W          # noqa: E402
import records as R        # noqa: E402
import verify as V         # noqa: E402
import ceiling as CL       # noqa: E402

RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))


def edge(v):
    return 0.5 - abs(v - round(v))


def tier(x):
    return "full" if x >= W.FULL_AT else ("pilot" if x >= W.PILOT_AT else "lapse")


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    A = R.build_all()
    rows = A["main_rows"]
    o = W.routes(rows)
    m = V.main_call(TARGET)
    cases = A["cases"]
    lot_cases = [c for c in cases if c.lottery]

    # ---------------------------------------------------------------- the chosen world and its family
    check("seed: the main seed passes the convergence and clearance screen", W.main_seed_ok(o), "seed %d" % R.MAIN_SEED)
    check("golden: the pack's cut equals the generator's", abs(m["cut"] - o["golden"]) < 1e-9, "%.4f" % m["cut"])
    check("golden: the call is the pilot's scale", tier(o["golden"]) == "pilot" and F["call"].endswith("pilot's scale"),
          "%.3f" % o["golden"])
    check("golden: the cut clears both thresholds by 3 points or more",
          o["golden"] - W.PILOT_AT >= 3 and W.FULL_AT - o["golden"] >= 3, "%.3f" % o["golden"])

    # ---------------------------------------------------------------- the semantic fork table
    check("SF1 the cut is the not-offered share less the offered share, in points",
          abs(o["golden"] - (o["not_offered"] - o["offered"])) < 1e-9 and o["golden"] > 0
          and tier(100 * (o["not_offered"] - o["offered"]) / o["not_offered"]) == "full",
          "relative reading %.1f per cent would file full scale" % (100 * (o["not_offered"] - o["offered"]) / o["not_offered"]))
    check("SF2 every listed defendant is in a denominator",
          o["n_offered"] + o["n_not_offered"] == o["n"] == m["n"] == len(lot_cases), "%d listed" % o["n"])
    check("SF3 the outcome at final disposition, not by the evaluation date",
          tier(o["naive"]) == "full" and tier(o["golden"]) == "pilot", "at the cut %.1f" % o["naive"])
    check("SF4 offered counts decliners: the participants-only contrast is another figure",
          round(o["participants_only"]) != round(o["golden"]), "participants only %.2f" % o["participants_only"])
    first_disp = Counter()
    for c in lot_cases:
        kinds = [k for d, k, t in c.events if k in R.DISPOSITION_CODES]
        if kinds:
            first_disp[kinds[0]] += 1
    check("SF5 every first disposition of a listed case is one of the coded kinds",
          set(first_disp) <= R.DISPOSITION_CODES and first_disp["DSR"] > 0, str(dict(first_disp)))
    last_leg = max(dt.datetime.strptime(r[2], "%m/%d/%Y").date() for r in A["legacy_ev"])
    last_cms = max(V.central_date(r[2]) for r in A["cms_ev"])
    check("SF6 no event after the evaluation date in either extract",
          last_leg < W.CUTOVER and last_cms <= W.CUT, "%s, %s" % (last_leg, last_cms))
    leg_dates = defaultdict(set)
    for r in A["legacy_ev"]:
        leg_dates[V.key(r[0])].add((dt.datetime.strptime(r[2], "%m/%d/%Y").date(), r[3]))
    mism = 0
    migrated = 0
    for r in A["cms_ev"]:
        if r[5] == "MIGRATED":
            migrated += 1
            if (V.central_date(r[2]), V.CMS_TO_KIND[r[3]]) not in leg_dates[V.key(r[0])]:
                mism += 1
    check("SF7 every migrated event carries its legacy date", migrated > 5000 and mism == 0,
          "%d migrated, %d off" % (migrated, mism))
    shift = 0
    for r in A["cms_ev"]:
        if r[3] in ("Pretrial Diversion Terminated - Restored to Calendar",) or r[3].startswith("Disposition") \
                or r[3].startswith("Dismissed"):
            if r[5] != "MIGRATED" and r[2][:10] != V.central_date(r[2]).isoformat():
                shift += 1
    check("SF8 terminations and dispositions are entered in office hours: UTC and local dates agree", shift == 0,
          "%d shifted" % shift)
    check("SF9 the not-offered arm's estimators agree to the whole per cent",
          len({round(o[k]) for k in ("not_offered", "not_offered_aj", "not_offered_matured")}) == 1,
          "%.3f %.3f %.3f" % (o["not_offered"], o["not_offered_aj"], o["not_offered_matured"]))
    check("SF10 the termination chance agrees across every participant's months and the matured terms",
          round(o["p_term"]) == round(o["p_term_matured"]), "%.3f %.3f" % (o["p_term"], o["p_term_matured"]))
    check("SF11 the terminated cases' conviction rate agrees across estimators",
          round(o["c_term"]) == round(o["c_term_aj"]), "%.3f %.3f" % (o["c_term"], o["c_term_aj"]))
    check("SF12 pooled and lottery-by-lottery contrasts agree to the whole point",
          round(o["fam_by_lottery"]) == round(o["golden"]), "%.3f %.3f" % (o["fam_by_lottery"], o["golden"]))
    check("SF13 case-by-case completion equals the arm-level construction (product-limit identity)",
          abs(o["fam_case_by_case"] - o["golden"]) < 1e-9, "%.6f" % (o["fam_case_by_case"] - o["golden"]))
    check("SF14 the cut from rounded shares equals the rounded cut",
          round(o["not_offered"]) - round(o["offered"]) == round(o["golden"]) == F["cut_points"],
          "%d - %d" % (round(o["not_offered"]), round(o["offered"])))
    bad = [c for c in lot_cases if sum(1 for d, k, t in c.events if k in R.DISPOSITION_CODES) > 1]
    check("SF15 every referred case ends once, on its own number", not bad, "%d with two endings" % len(bad))
    term_mis = 0
    for p in A["parts"]:
        c = p["case"]
        dva = [t for d, k, t in c.events if k == "DVA"]
        if not dva or R.fmt_term(c) not in dva[0]:
            term_mis += 1
    check("SF16 the docket's term equals the provider's term for every participant", term_mis == 0,
          "%d off" % term_mis)
    check("SF17 the decliners complete at their own disposed rate under every estimator",
          round(o["offered"]) == round(o["offered_aj"]) == round(o["offered_matured"]),
          "%.3f %.3f %.3f" % (o["offered"], o["offered_aj"], o["offered_matured"]))
    # SF18: the clock. Day-based product limit from the term start agrees; from the agreement filing it does not.
    parts = [r for r in rows if r["path"] in ("terminated", "completed")]

    def km_from(origin):
        T, E = [], []
        for r in parts:
            t0 = r[origin]
            if r["path"] == "terminated" and r["term_date"] <= W.CUT:
                T.append((r["term_date"] - t0).days)
                E.append(1)
            elif r["path"] == "completed" and r["term_end"] <= W.CUT:
                T.append((r["term_end"] - t0).days)
                E.append(0)
            else:
                T.append((W.CUT - t0).days)
                E.append(0)
        ordr = np.argsort(T, kind="stable")
        t = np.array(T)[ordr]
        e = np.array(E)[ordr]
        S = 1.0
        i = 0
        while i < len(t):
            j = i
            while j < len(t) and t[j] == t[i]:
                j += 1
            S *= 1 - e[i:j].sum() / (len(t) - i)
            i = j
        return 100 * (1 - S)

    def cut_with(pt):
        return o["not_offered"] - (o["p_decline"] / 100 * o["c_declined"] + (1 - o["p_decline"] / 100) * pt / 100 * o["c_term"])

    pt_ts, pt_ag = km_from("term_start"), km_from("agree")
    check("SF18 the termination chance on the term's clock agrees in days and months",
          round(pt_ts) == round(o["p_term"]) and round(cut_with(pt_ts)) == round(o["golden"]), "%.3f" % pt_ts)
    check("SF18 timed from the agreement filing, completions censored at uneven term ends, it files another tier",
          tier(cut_with(pt_ag)) != "pilot", "%.2f points" % cut_with(pt_ag))

    # SF23: a term that ends on the cut. Its final reviews are in the docket before the cut and the provider's
    # August report shows every other member completed on the term's last day, so the review is behind them.
    from openpyxl import load_workbook
    p_ev = V.read_events(TARGET)
    p_recs = [dict(r, **V.case_state(p_ev[r["key"]])) for r in V.read_roster(TARGET)]
    p_par = [x for x in p_recs if x["offered"] and x["term_start"]]
    last = [x for x in p_par if V.months_between(x["term_start"], W.CUT) + 1 == 12]
    rev = [x for x in last if x["terminated_on"] and V.months_between(x["term_start"], x["terminated_on"]) + 1 == 12]
    rest = {x["key"] for x in last if not x["terminated_on"]}
    ws = load_workbook(os.path.join(TARGET, "nethercote_reports", "NCJS_Larkmoor_Participants_2026-08.xlsx"),
                       read_only=True).active
    rws = [list(r) for r in ws.iter_rows(values_only=True)]
    hi = next(i for i, r in enumerate(rws) if r and r[0] == "Participant ID")
    seen = {}
    for r in rws[hi + 1:]:
        if r and r[0] and str(r[0]).startswith("P"):
            d = dict(zip(rws[hi], r))
            seen[V.key(d["Case Number"])] = (d["Status"], str(d["Discharge Date"])[:10])
    done = [k for k in rest if seen.get(k) == ("Completed", W.CUT.isoformat())]
    hz = [t[3] for t in m["table"]]

    def p_term_cases(review_ahead):
        tot = 0.0
        for x in p_par:
            if x["terminated_on"]:
                tot += 1
                continue
            e = V.months_between(x["term_start"], W.CUT) + 1
            if review_ahead and x["key"] in rest:
                e = 11
            S = 1.0
            for j in range(e + 1, 13):
                S *= 1 - hz[j - 1]
            tot += 1 - S
        return 100 * tot / len(p_par)

    ahead, behind = cut_with(p_term_cases(True)), cut_with(p_term_cases(False))
    check("SF23 the cohort whose term ends on the cut has its final reviews in the docket before the cut",
          rev and max(x["terminated_on"] for x in rev) <= W.CUT, "%d of %d terminated at the review" % (len(rev), len(last)))
    check("SF23 the provider's August report shows every other member of that cohort completed on 31 August 2026",
          rest and len(done) == len(rest), "%d of %d" % (len(done), len(rest)))
    check("SF23 case by case with the review behind them equals the golden; with it still ahead, the same call",
          abs(behind - o["golden"]) < 1e-3 and tier(ahead) == "pilot",
          "behind %.4f, golden %.4f, ahead %.2f" % (behind, o["golden"], ahead))

    # ---------------------------------------------------------------- R1, R2, R3: the client's three rules
    hdrs = {}
    for f in ("legacy_docket_events_2025_2026.csv", "cms_docket_events_2026.csv", "legacy_case_charges.csv",
              "cms_case_charges.csv"):
        with open(os.path.join(TARGET, f)) as fh:
            hdrs[f] = next(csv.reader(fh))
    flat = " ".join(" ".join(h) for h in hdrs.values()).lower()
    check("R1 the raw material ships: lottery assignment records and dated case events, no outcome column",
          os.path.exists(os.path.join(TARGET, "diversion_lottery_draws_2025_2026.xlsx"))
          and not re.search(r"convict|outcome|final|eventual|terminat", flat), str(list(hdrs)))
    check("R1 the golden's decisive computation reads the docket's own events (the verifier rebuilds it from them)",
          abs(m["p_term"] - o["p_term"]) < 1e-9 and m["table"][11][2] > 20, "month 12: %s" % (m["table"][11],))
    # R2: each mess item, mishandled the natural way, leaves the call and its components where they were
    tmp = tempfile.mkdtemp()
    try:
        shutil.copytree(TARGET, os.path.join(tmp, "p"))
        P = os.path.join(tmp, "p")
        # clerk re-entries kept twice: the verifier's per-case logic already ignores repeats
        rows_leg = list(csv.reader(open(os.path.join(P, "legacy_docket_events_2025_2026.csv"))))
        n_dup = len(rows_leg) - 1 - len({tuple(r) for r in rows_leg[1:]})
        check("R2 clerk re-entries are present and real (duplicate legacy rows)", 200 < n_dup < 1500, "%d" % n_dup)
        # the UTC clock read as local time
        rows_cms = list(csv.reader(open(os.path.join(P, "cms_docket_events_2026.csv"))))
        orig = V.central_date
        V.central_date = lambda s: dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").date()
        try:
            m_utc = V.main_call(P)
        finally:
            V.central_date = orig
        check("R2 the new system's UTC stamps read as local dates leave the call and components unchanged",
              all(round(m_utc[k]) == round(m[k]) for k in ("cut", "c_no", "offered", "p_term", "c_term")),
              "cut %.3f" % m_utc["cut"])
        # migrated duplicates kept (no dedup across extracts): count both copies as separate events
        check("R2 events in both extracts carry one date, so keeping both copies changes no case's ending",
              mism == 0, "migrated %d" % migrated)
        # case numbers left unnormalised: the roster's legacy numbers find none of the new system's numbers
        cms_nums = {r[0] for r in rows_cms[1:]}
        ros = V.read_roster(P)
        hits = 0
        from openpyxl import load_workbook
        wb = load_workbook(os.path.join(P, "diversion_lottery_draws_2025_2026.xlsx"), read_only=True)
        listed = [r[0] for ws in wb.worksheets for r in ws.iter_rows(values_only=True)
                  if r and r[0] and re.match(r"^(LC|BW|WM|SH)\d", str(r[0]))]
        hits = sum(1 for x in listed if x in cms_nums)
        check("R2 an exact-string join of the roster to the new system matches no legacy-numbered case, so the "
              "unnormalised join cannot pass silently", hits == 0 and len(listed) > 2500, "%d listed" % len(listed))
        # the legacy date format read day-first fails outright on days above twelve
        fails = 0
        sample = rows_leg[1::97]
        for r in sample:
            try:
                dt.datetime.strptime(r[2], "%d/%m/%Y")
            except ValueError:
                fails += 1
        check("R2 legacy dates read day-first fail to parse on most rows", fails > 0.5 * len(sample),
              "%d of %d" % (fails, len(sample)))
        # the provider's workbooks, the charges files and the distractors deleted: the call does not move
        for f in ("legacy_case_charges.csv", "cms_case_charges.csv", "county_jail_population_2025_2026.csv",
                  "district_court_annual_statistics_fy2025.pdf", "penal_code_conversion_table_2026.csv"):
            os.remove(os.path.join(P, f))
        shutil.rmtree(os.path.join(P, "nethercote_reports"))
        m_del = V.main_call(P)
        check("R2 the call and every component are identical with every ask file and distractor deleted",
              all(abs(m_del[k] - m[k]) < 1e-9 for k in ("cut", "c_no", "offered", "p_term", "c_term")), "")
    finally:
        shutil.rmtree(tmp)
    # distractor deletion for the asks
    tmp = tempfile.mkdtemp()
    try:
        shutil.copytree(TARGET, os.path.join(tmp, "p"))
        P = os.path.join(tmp, "p")
        for f in ("county_jail_population_2025_2026.csv", "district_court_annual_statistics_fy2025.pdf"):
            os.remove(os.path.join(P, f))
        a_del = V.asks(P)
        check("distractors: every ask figure is unchanged with both distractors deleted",
              a_del["cls"] == F["filings_by_class"] and a_del["div"] == F["filings_by_division"]
              and a_del["hours"] == F["hours_by_site"] and a_del["rest"] == F["restitution_by_site"], "")
    finally:
        shutil.rmtree(tmp)
        CL.PACK = TARGET
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("distractors: two named in metadata.json and present in the pack",
          len(meta["distractors"]) >= 2 and all(os.path.exists(os.path.join(TARGET, d)) for d in meta["distractors"]),
          str(meta["distractors"]))
    # R3a: the analyst test on the clean truth
    check("R3a the easy route, recorded convictions by lottery result, files full scale", tier(o["naive"]) == "full",
          "%.2f" % o["naive"])
    check("R3a the field's censoring reflex, cumulative incidence at the longest follow-up, files full scale",
          tier(o["cif_max"]) == "full" and tier(o["cif_365"]) == "full", "%.2f, %.2f" % (o["cif_max"], o["cif_365"]))
    check("R3a cases that have ended, taken alone, file a lapse", tier(o["complete_case"]) == "lapse",
          "%.2f" % o["complete_case"])
    # R3b: the decisive step alone moves the easy route to the golden; each lower correction alone does not
    check("R3b completing the offered arm through the program's own stages files the golden tier",
          tier(o["golden"]) == "pilot" and tier(o["fam_case_by_case"]) == "pilot", "")
    for k in ("terminated_so_far", "terminated_like_not_offered", "term_without_final_review", "terminated_convicted_so_far",
              "matured_lotteries_at_cut", "exits_so_far"):
        check("R3b the partial correction '%s' stays off the golden tier" % k, tier(o[k]) != "pilot", "%.2f" % o[k])
    cheap = [k for k in ("naive", "complete_case", "cif_365", "cif_425", "cif_max", "matured_lotteries_at_cut",
                         "terminated_so_far", "terminated_like_not_offered", "term_without_final_review",
                         "terminated_convicted_so_far", "exits_so_far") if tier(o[k]) == "pilot"]
    check("Gate F: no route that skips the stage-wise completion lands the call", not cheap, str(cheap))
    # R3c: no plant
    sizes = [len(v) for v in A["roster"].values()]
    nums = [x[0] for v in A["roster"].values() for x in v]
    flags = ["".join(x[5] for x in v) for v in A["roster"].values()]
    check("R3c no copied block: no case on two lists, no offer pattern repeated, list sizes vary",
          len(nums) == len(set(nums)) and len(set(flags)) == len(flags) and len(set(sizes)) >= 10, str(sorted(sizes)))
    docs = V.documents(TARGET)
    planted = [n for n, t in docs.items() if re.search(r"percentage points? (?:lower|reduction) of \d|recommend", t, re.I)]
    check("R3c no document states an effect or argues a tier", not planted, str(planted))

    # ---------------------------------------------------------------- ladder margins and edges
    for k in ("naive", "cif_365", "cif_max", "terminated_so_far", "terminated_like_not_offered",
              "term_without_final_review", "terminated_convicted_so_far", "matured_lotteries_at_cut"):
        check("ladder: '%s' clears the full-scale threshold by 2 points or more" % k, o[k] >= W.FULL_AT + 2, "%.2f" % o[k])
    for k in ("complete_case", "exits_so_far"):
        check("ladder: '%s' sits 4 points or more below the pilot floor" % k, o[k] <= W.PILOT_AT - 4, "%.2f" % o[k])
    for name, v in (("cut", o["golden"]), ("not offered", o["not_offered"]), ("offered", o["offered"]),
                    ("termination chance", o["p_term"]), ("terminated convicted", o["c_term"]),
                    ("declined share", o["p_decline"]), ("declined convicted", o["c_declined"]),
                    ("final review", o["final_review_rate"]),
                    ("recorded not offered", o["recorded_not_offered"]), ("recorded offered", o["recorded_offered"])):
        check("edge: %s sits 0.15 or more from its whole-per-cent edge" % name, edge(v) >= 0.15, "%.3f" % v)

    # ---------------------------------------------------------------- asks: devices forced, separated, measured
    fy = lambda d: W.FY_START <= d <= W.FY_END
    truth_cls = Counter(c.charges[0][1] for c in cases if fy(c.filed) and c.charges[0][1])
    check("ask F: the golden reading of the sections recovers the true class counts",
          {W.CLASS_NAME[k]: v for k, v in truth_cls.items()} == F["filings_by_class"], "")
    reps_jan_all = [r for r in CL.load_reports() if r["month"] == dt.date(2026, 1, 1)]
    conv = {o_[2]: o_[3] for o_ in W.OFFENCES}
    leg = {V.key(r[0]): r for r in A["legacy_ch"] if r[8] == "1"}
    def as_2026(lr):
        offence = dt.datetime.strptime(lr[7], "%m/%d/%Y").date()
        return conv[lr[9]] if offence < W.RECODE else lr[9]
    agree_conv = sum(1 for r in A["cms_ch"] if r[7] == "1" and V.key(r[0]) in leg and r[8] == as_2026(leg[V.key(r[0])]))
    both = sum(1 for r in A["cms_ch"] if r[7] == "1" and V.key(r[0]) in leg)
    check("SF19 ask F: every case in both charge extracts carries the conversion of its legacy section in the new system",
          both > 1500 and agree_conv == both, "%d of %d" % (agree_conv, both))
    old_set, new_set = set(conv), set(conv.values())
    bad_num = 0
    n_2026 = 0
    for r in A["legacy_ch"]:
        filed = dt.datetime.strptime(r[3], "%m/%d/%Y").date()
        if filed < W.RECODE:
            continue
        n_2026 += 1
        offence = dt.datetime.strptime(r[7], "%m/%d/%Y").date()
        if (offence < W.RECODE and r[9] not in old_set) or (offence >= W.RECODE and r[9] not in new_set):
            bad_num += 1
    check("SF19 legacy filings of 2026 carry the numbering in force on their offense date, without exception",
          n_2026 > 1000 and bad_num == 0, "%d rows, %d off" % (n_2026, bad_num))
    jan = Counter()
    for p_ in A["parts"]:
        jan[p_["site"]] += sum(a_ for d_, a_ in p_["pays"] if d_.year == 2026 and d_.month == 1)
    jan_rep = Counter()
    for rep in reps_jan_all:
        for x in rep["recs"]:
            jan_rep[x["site"]] += x["rest"] / (0.95 if rep["system"] == "new" else 1.0)
    check("SF22 each January payment sits in exactly one of the two January reports",
          all(abs(jan_rep[s_] - jan[s_]) < 0.01 for s_ in W.SITES), str({k: round(v, 2) for k, v in jan_rep.items()}))
    old_only = set(conv) - set(conv.values())
    late = sum(1 for r in A["legacy_ch"] if dt.datetime.strptime(r[3], "%m/%d/%Y").date() >= W.RECODE and r[9] in old_only)
    check("ask F: some cases filed in 2026 cite a section only the 2025 numbering has (the offense-date tell)",
          late > 20, "%d rows" % late)
    shared = set(conv) & set(conv.values())
    check("ask F: reused section numbers reach every eligible class",
          {W.NEW_CLASS.get(s) for s in shared} >= set("ABCDE"), str(sorted(shared)))
    for label, rule in (("the dated mapping (cracker)", CL.rule_filing_date),
                        ("the conversion alone", CL.rule_conversion_aware),
                        ("the offense date alone", CL.rule_offence_date)):
        c_, d_ = CL.filings(rule)
        moved_c = sum(1 for k, v in F["filings_by_class"].items() if c_.get(k) != v)
        moved_d = sum(1 for k, v in F["filings_by_division"].items() if d_.get(k) != v)
        check("ask F: %s moves every class and every division" % label, moved_c == 5 and moved_d == 4,
              "%d classes, %d divisions" % (moved_c, moved_d))
    h_c, r_c = CL.provider(dict(hours="as_given"))
    h_d, _ = CL.provider(dict(hours="difference"))
    _, r_j = CL.provider(dict(hours="cumulative", sum_january=True))
    _, r_g = CL.provider(dict(hours="cumulative", gross_up=True))
    check("ask H: the running totals summed as given miss every site", all(h_c[s] != F["hours_by_site"][s] for s in W.SITES), "")
    check("ask H: the running totals differenced within the new system miss every site",
          all(h_d[s] != F["hours_by_site"][s] for s in W.SITES), str(h_d))
    check("ask R: the January halves deduplicated miss every site", all(r_c[s] != F["restitution_by_site"][s] for s in W.SITES), "")
    check("ask R: the January halves summed without the gross-up miss every site",
          all(r_j[s] != F["restitution_by_site"][s] for s in W.SITES), str(r_j))
    check("ask R: the gross-up with the January halves deduplicated misses every site",
          all(r_g[s] != F["restitution_by_site"][s] for s in W.SITES), str(r_g))
    # the provider's tells, as the files carry them
    reps = CL.load_reports()
    jan_old = [r for r in reps if r["system"] == "old" and r["month"] == dt.date(2026, 1, 1)]
    new_reps = [r for r in reps if r["system"] == "new"]
    cum_ok = True
    last = {}
    for rep in sorted(new_reps, key=lambda r: r["month"]):
        for x in rep["recs"]:
            if x["hours"] + 1e-9 < last.get(x["key"], 0):
                cum_ok = False
            last[x["key"]] = x["hours"]
    check("SF21 ask H: the new system's hours never fall for a participant and never pass 40", cum_ok and max(last.values()) <= 40,
          "max %.1f" % max(last.values()))
    cents = [x["rest"] for rep in new_reps for x in rep["recs"] if x["rest"]]
    exact = all(abs(round(v / 0.95, 6) - round(v / 0.95)) < 1e-6 for v in cents)
    check("SF20 ask R: every new-system restitution amount is 95 per cent of a whole-dollar payment", exact and len(cents) > 500,
          "%d amounts" % len(cents))
    check("SF22 ask R: one old-system January report ships beside the new system's January report",
          len(jan_old) == 1 and len(jan_old[0]["recs"]) > 500
          and len([r for r in new_reps if r["month"] == dt.date(2026, 1, 1)]) == 1, "%d rows" % len(jan_old[0]["recs"]))
    # the separation line: the call reads none of the asks' files and none of their columns
    check("separation: the verifier's main call opens only the roster and the two docket extracts",
          set(re.findall(r'"([a-z_0-9]+\.(?:csv|xlsx))"', open(os.path.join(HERE, "verify.py")).read().split("def asks")[0]))
          == {"diversion_lottery_draws_2025_2026.xlsx", "legacy_docket_events_2025_2026.csv", "cms_docket_events_2026.csv"}, "")

    # ---------------------------------------------------------------- input gates and the realism sweep
    files = [p for p in glob.glob(os.path.join(TARGET, "**", "*"), recursive=True) if os.path.isfile(p)]
    exts = Counter(os.path.splitext(p)[1] for p in files)
    big = max(sum(1 for _ in open(p)) for p in files if p.endswith(".csv"))
    check("gate: ten or more files", len(files) >= 10, "%d files" % len(files))
    check("gate: three or more formats", len(exts) >= 3, str(dict(exts)))
    check("gate: a file of 25,000 rows or more", big >= 25000, "%d rows" % big)
    describing = [p for p in files if re.search(r"readme|dictionary|codebook|manifest|field.?notes|notes", os.path.basename(p), re.I)]
    check("gate: no describing file ships", not describing, str(describing))
    check("realism: client numbers are not an arithmetic sequence",
          len({b - a for a, b in zip(*(lambda s: (s, s[1:]))(sorted(int(p["client_no"][1:]) for p in A["parts"])))}) > 1, "")
    seqs = defaultdict(list)
    for c in cases:
        if c.number_legacy:
            seqs[c.number_legacy[:6]].append(int(c.number_legacy[6:]))
    big_series = [v for v in seqs.values() if len(v) >= 200]
    gapped = sum(1 for v in big_series if len(set(np.diff(sorted(v)))) > 1)
    check("realism: every case number series of 200 or more carries the gaps of sealed cases",
          gapped == len(big_series) and len(big_series) >= 8, "%d of %d series" % (gapped, len(big_series)))
    tot = [F["filings_total"]] + list(F["filings_by_class"].values()) + list(F["hours_by_site"].values()) + list(F["restitution_by_site"].values())
    check("realism: no headline total is round", all(v % 100 != 0 for v in tot), str(tot))
    ref = {l.strip().lower() for l in open(os.path.join(HERE, "h21_reference_places.txt")) if l.strip()}

    def near(a, b):
        if abs(len(a) - len(b)) > 2:
            return False
        prev = list(range(len(b) + 1))
        for i, ca in enumerate(a, 1):
            cur = [i]
            for j, cb in enumerate(b, 1):
                cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
            prev = cur
        return prev[-1] <= 2

    inv = ["larkmoor", "bramwick", "wendmoor", "strandham", "nethercote"]
    clash = [n for n in inv for r in ref if near(n, r) or (len(r) > 4 and r in n)]
    check("realism: invented places clear the place register (edit distance two, containment)", not clash, str(clash[:5]))
    card = json.load(open(os.path.join(TASK, "..", ".claude", "skills", "fingerprint", "cards", "task274.json")))
    people = card["world"]["people"]
    alltext = " ".join(docs.values())
    named = [p for p in ("Melanie Nielsen", "Roy Goodwin", "Natalie Hansen") if p in alltext or p.split()[1] in alltext]
    check("realism: every persona named in the pack is a drawn persona", all(n in people for n in named), str(named))
    check("realism: the resolution predates the pilot and the policy predates the 2026 lists",
          "Adopted 22 April 2025" in docs["board_resolution_2025_31.pdf"] and "Effective 1 January 2026" in docs["policy"], "")
    check("verify: the independent verifier reproduces every figure from the pack", V.main(["--pack", TARGET]) == 0, "")

    fails = [r for r in RESULTS if not r[1]]
    for label, ok, detail in RESULTS:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    print("%d assertions, %d failed" % (len(RESULTS), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
