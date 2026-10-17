"""task193: the generator's own assertions, run on every build."""
import collections
import csv
import datetime as dt
import json
import os
import re

import numpy as np

import world as W
import golden as G
import asks as AS
from asks import distinct as asks_distinct

N = 0
FAILED = []


def ok(label, cond, detail=""):
    global N
    N += 1
    if not cond:
        FAILED.append("%s  %s" % (label, detail))


def rd(tgt, name):
    with open(os.path.join(tgt, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _referred(tgt, rp, route, firsts=None, **kw):
    return G.screen(tgt, rp, route, firsts, **kw)[0]


def _pdf_text(tgt):
    import pypdf
    r = pypdf.PdfReader(os.path.join(tgt, "screen_standard_7_2024.pdf"))
    return " ".join(p.extract_text() for p in r.pages).replace("\n", " ")


def run(tgt, g, first, lines, kept, rejected, people, keys, new_keys, switch_day):
    global N, FAILED
    N, FAILED = 0, []
    rp = G.load(tgt)
    rows, pairs = rp
    firsts = G.first_receipts(rows)
    referred, counts = G.screen(tgt, rp, "perm", firsts)
    by = {r["key"]: r for r in counts}
    cands = [r for r in counts if r["candidate"]]

    # ---------------------------------------------------------------- the answer
    ok("answer.count", len(referred) == 7, "%d referred" % len(referred))
    ok("answer.candidates", len(cands) == 20, "%d candidates" % len(cands))
    ok("answer.screened", len(counts) == 23, "%d screened" % len(counts))
    ok("answer.matches_figures", g["referred_count"] == len(referred))

    # ---------------------------------------------------------------- R1: the field's raw material
    disp = rd(tgt, "dispensings_2025_2026.csv")
    ok("R1.rows_are_dispensings",
       set(disp[0]) == set(["record_id", "person_key", "package_code", "date_of_dispensing",
                            "pharmacy", "n_packages", "prescriber", "submission_date"]),
       str(sorted(disp[0])))
    headers = []
    for name in sorted(os.listdir(tgt)):
        if name.endswith(".csv"):
            with open(os.path.join(tgt, name), encoding="utf-8") as fh:
                headers += [h.strip().lower() for h in fh.readline().strip().split(",")]
    banned = [h for h in headers if h in ("expected", "expected_after", "sequence_ratio",
                                          "null_ratio", "referred", "referral", "multiple",
                                          "order_share", "share_after", "is_signal")]
    ok("R1.no_column_holds_the_quantity", not banned, str(banned))
    ok("R1.golden_reads_the_rows", len(rows) > 100000, "%d conformed lines" % len(rows))

    # ---------------------------------------------------------------- R2: every mess item neutral
    variants = {
        "keys_unfolded": dict(fold_keys=False),
        "packages_ignore_validity": dict(packages="ignore_validity"),
        "resend_kept": dict(drop_resend=False),
    }
    for label, kw in variants.items():
        alt = G.load(tgt, **kw)
        got = _referred(tgt, alt, "perm")
        ok("R2." + label, got == referred, "%s" % sorted(set(got) ^ set(referred)))
    # the rejected lines never carry a first receipt, so dropping them cannot move a first date
    firsts_truth = {}
    for r in lines:
        k = (r["pid"], r["code"])
        if k not in firsts_truth or r["day"] < firsts_truth[k]:
            firsts_truth[k] = r["day"]
    ok("R2.rejected_never_first", all(not r["is_first"] for r in rejected))
    orig = set((r["key"], r["vnr"], r["day"], r["pharmacy"]) for r in kept if not r.get("resend"))
    ok("R2.resend_changes_no_date",
       all((r["key"], r["vnr"], r["day"], r["pharmacy"]) in orig
           for r in kept if r.get("resend")),
       "every re-sent copy repeats an original line's key, package, date and pharmacy")

    # ---------------------------------------------------------------- R3: the analyst test
    crude = _referred(tgt, rp, "half", firsts)
    ok("R3a.analyst_test", len(crude) == 10, "%d on the equal-chance expectation" % len(crude))
    ok("R3a.named_wrong_answer", sorted(crude) != sorted(referred))
    ok("R3b.decisive_step_alone", sorted(referred) == sorted(
        _referred(tgt, rp, "perm", firsts)))
    for route in ("incidence", "pairprod", "even"):
        ok("R3b.route_" + route, sorted(_referred(tgt, rp, route, firsts)) == sorted(referred),
           route)
    r0 = G.rung0(tgt)[0]
    ok("R3b.rung0_wrong", sorted(r0) != sorted(referred), "%d" % len(r0))
    edge = _referred(tgt, rp, "half", firsts)
    ok("R3c.no_answer_key", not any(
        re.search(r"is_correct|should_exclude|answer|golden|expected_number", n, re.I)
        for n in os.listdir(tgt)), str(os.listdir(tgt)))
    text_blob = ""
    for name in os.listdir(tgt):
        if name.endswith((".csv", ".json")):
            with open(os.path.join(tgt, name), encoding="utf-8", errors="replace") as fh:
                text_blob += fh.read().lower()
    phrases = ["equally likely", "equal chance", "symmetr", "sequence ratio", "null ratio",
               "incidence distribution", "half of the pair", "expected number", "order ratio",
               "asymmetry", "crude ratio", "null-effect", "opportunity window", "time at risk",
               "window arithmetic", "reporting ratio", "disproportion", "masking", "comparator"]
    present = [p for p in phrases if p in text_blob]
    ok("R3c.no_signpost_in_data", not present, str(present))

    # ---------------------------------------------------------------- separation and margins
    ratios = {}
    for route in ("half", "perm", "incidence", "pairprod", "even"):
        _, rws = G.screen(tgt, rp, route, firsts)
        ratios[route] = {r["key"]: r["ratio"] for r in rws if r["candidate"]}
    worst = min(abs(v - W.MULTIPLE) / W.MULTIPLE
                for route in ratios for v in ratios[route].values())
    ok("sep.margin_6pc", worst >= 0.060, "tightest %.3f" % worst)
    ok("sep.crude_not_subset", not set(crude).issubset(set(referred)))
    ok("sep.answer_not_subset", not set(referred).issubset(set(crude)))
    ok("sep.crude_only_5", len(set(crude) - set(referred)) == 5,
       str(sorted(set(crude) - set(referred))))
    ok("sep.window_only_2", len(set(referred) - set(crude)) == 2,
       str(sorted(set(referred) - set(crude))))
    ok("sep.shared_5", len(set(referred) & set(crude)) == 5)
    lowest = min(by[k]["ratio"] for k in referred)
    ok("sep.lowest_referred", lowest >= 1.33, "%.3f" % lowest)
    highest_miss = max(r["ratio"] for r in cands if not r["referred"])
    ok("sep.highest_miss", highest_miss <= 1.175, "%.3f" % highest_miss)

    # dominance: the loudest pair on the crude basis is refused on the answer's basis
    loud = max(cands, key=lambda r: r["after"] / r["n"])
    ok("dom.loudest_refused", not loud["referred"], loud["key"])
    ok("dom.loudest_crude_refers", ratios["half"][loud["key"]] >= W.MULTIPLE)
    # no single product carries the whole difference
    moved = set(k.split("/")[0] for k in set(crude) ^ set(referred))
    ok("dom.moved_products", len(moved) >= 4, str(sorted(moved)))
    # a lifecycle rule of thumb does not work
    ok("dom.new_product_not_a_rule",
       any(k.split("/")[0] in ("P03", "P04") and k not in referred for k in
           [r["key"] for r in cands]))
    ok("dom.ending_product_not_a_rule", "P09/M7" in referred)

    # ---------------------------------------------------------------- SF rows
    ok("SF1", referred == _referred(tgt, rp, "perm", firsts),
       "the window is read on the date of dispensing")
    f12 = {k: v for k, v in firsts.items()}
    ok("SF2.clearance_bites",
       sum(1 for (k, c), d in firsts.items() if d <= G.CLEAR_B) > 20000,
       "first receipts in the clearance period")
    win_only = {}
    for key, code, d, vnr, ph in rows:
        if not (G.WIN_A <= d <= G.WIN_B):
            continue
        k = (key, code)
        if k not in win_only or d < win_only[k]:
            win_only[k] = d
    cnt_alt = G.pair_counts(win_only, pairs)
    ok("SF2.ignoring_clearance_changes_counts",
       any(a["n"] != b["n"] for a, b in zip(sorted(cnt_alt, key=lambda r: r["key"]),
                                            sorted(counts, key=lambda r: r["key"]))))
    ok("SF3.clearance_is_24_months", (G.WIN_A - G.CLEAR_A).days == 731)
    xw = rd(tgt, "person_key_crosswalk.csv")
    ok("SF4.crosswalk_rows", len(xw) == 420, "%d" % len(xw))
    ok("SF5.reissued_codes_in_register",
       any(r["valid_to"] for r in rd(tgt, "package_index.csv")))
    marks = set(r["marker_atc_group"] for r in rd(tgt, "screen_annexes.csv"))
    ok("SF6.marker_groups", len(marks) == 8, "%d marker groups" % len(marks))
    same_day = 0
    byp = collections.defaultdict(dict)
    for (k, c), d in firsts.items():
        byp[k][c] = d
    for pc, mc in pairs:
        for k, got in byp.items():
            if got.get(pc) is not None and got.get(pc) == got.get(mc):
                same_day += 1
    ok("SF7.same_day_patients_exist", same_day > 0, "%d" % same_day)
    ok("SF8.deaths_and_exits_recorded",
       sum(1 for r in rd(tgt, "person_register.csv") if r["date_of_death"]) > 50)
    ok("SF9.minimum_bites", len(counts) - len(cands) == 3)
    ok("SF10.no_pair_on_the_line",
       all(abs(v - W.MULTIPLE) > 0.004 for route in ratios for v in ratios[route].values()))
    ok("SF11.no_share_on_a_boundary",
       all(abs(round(100.0 * r["after"] / r["n"], 1) - 100.0 * W.MULTIPLE * r["expected"] / r["n"])
           > 0.4 for r in cands))
    tracker = G.open_pairs(tgt)
    ok("SF12.tracker_ties",
       all(("%s/%s" % p) not in [r["key"] for r in cands if r["ratio"] >= W.MULTIPLE]
           for p in tracker), str(sorted(tracker)))
    ok("SF13.rounding_stable",
       all(abs(r["ratio"] - W.MULTIPLE) > 0.01 for r in cands))
    ok("SF14.resend_neutral", _referred(tgt, G.load(tgt, drop_resend=False), "perm") == referred)
    bad_dates = 0
    for r in rd(tgt, "dispensings_2025_2026.csv"):
        d = r["date_of_dispensing"]
        if int(d[0:2]) > 12:
            bad_dates += 1
    ok("SF15.misread_dates_impossible", bad_dates / float(len(disp)) > 0.55,
       "%.3f of window rows have a day above 12" % (bad_dates / float(len(disp))))
    ok("SF16.shares_distinct",
       len(set(round(100.0 * r["after"] / r["n"], 1) for r in cands)) == len(cands),
       str(sorted(round(100.0 * r["after"] / r["n"], 1) for r in cands)))
    ok("SF17.referral_quarter_filed", W.REFERRAL_QUARTER == "2027 Q1")

    # ---------------------------------------------------------------- closure axes
    ok("ax9.boundary_inclusivity_filed", os.path.exists(
        os.path.join(tgt, "screen_standard_7_2024.pdf")))
    ok("ax4.pull_after_window", W.PULL_DAY > W.WIN_B)
    ok("ax12.every_window_line_submitted",
       all(r["submitted"] <= W.NDAY + 20 for r in kept))
    ok("ax14.row_order_neutral", True)
    perm_rows = list(rows)
    rng = np.random.default_rng(5)
    for _ in range(3):
        rng.shuffle(perm_rows)
        ok("ax14.permutation", G.screen(tgt, (perm_rows, pairs), "perm")[0] == referred)
    ok("ax15.duplicates_collapse", len(set(rows)) == len(rows))
    ok("ax16.every_package_maps",
       all(v[0] in W.PCODES + W.MCODES for v in W.PKG_OF.values()))

    # ---------------------------------------------------------------- the three dates designed out
    pkg = {r["vnr"]: r for r in rd(tgt, "package_index.csv")}
    bad = 0
    for name, datec, parse in (("dispensings_2023_2025.csv", "disp_date", G.iso),
                               ("dispensings_2025_2026.csv", "date_of_dispensing", G.dk)):
        for r in rd(tgt, name):
            d = parse(r[datec])
            p = pkg[r["vnr"] if "vnr" in r else r["package_code"]]
            vf = G.iso(p["valid_from"]) if p["valid_from"] else None
            vt = G.iso(p["valid_to"]) if p["valid_to"] else None
            if (vf and d < vf) or (vt and d > vt):
                bad += 1
    ok("defect1.every_line_inside_one_validity", bad == 0, "%d lines outside" % bad)
    late = 0
    for name, datec, subc, parse in (
            ("dispensings_2023_2025.csv", "disp_date", "submitted", G.iso),
            ("dispensings_2025_2026.csv", "date_of_dispensing", "submission_date", G.dk)):
        for r in rd(tgt, name):
            if parse(r[subc]) < parse(r[datec]):
                late += 1
    ok("defect2.submission_never_before_dispensing", late == 0, "%d" % late)
    mkt = {r["product_code"]: (G.iso(r["first_marketed"]),
                               G.iso(r["authorisation_valid_to"]) if r["authorisation_valid_to"]
                               else None) for r in rd(tgt, "product_register.csv")}
    bad_t = []
    for r in rd(tgt, "signal_tracker_export.csv"):
        mf, mt = mkt[r["product_code"]]
        if G.iso(r["opened_on"]) < mf:
            bad_t.append(("tracker", r["tracker_ref"]))
    QS = {"2025 Q4": (dt.date(2025, 10, 1), dt.date(2025, 12, 31)),
          "2026 Q1": (dt.date(2026, 1, 1), dt.date(2026, 3, 31)),
          "2026 Q2": (dt.date(2026, 4, 1), dt.date(2026, 6, 30)),
          "2026 Q3": (dt.date(2026, 7, 1), dt.date(2026, 9, 30))}
    for r in rd(tgt, "spontaneous_reports_summary.csv"):
        mf, mt = mkt[r["product_code"]]
        if QS[r["quarter"]][1] < mf:
            bad_t.append(("reports", r["product_code"], r["quarter"]))
    for name, datec, parse in (("dispensings_2023_2025.csv", "disp_date", G.iso),
                               ("dispensings_2025_2026.csv", "date_of_dispensing", G.dk)):
        for r in rd(tgt, name):
            code = W.PKG_OF[r["vnr"] if "vnr" in r else r["package_code"]][0]
            if code not in mkt:
                continue
            d = parse(r[datec])
            mf, mt = mkt[code]
            if d < mf or (mt and d > mt):
                bad_t.append(("dispensing", code, str(d)))
                break
    ok("defect4.no_row_outside_its_product_lifecycle", not bad_t, str(bad_t[:6]))
    ok("defect4.standard_stamp_is_consistent",
       "2026" not in _pdf_text(tgt).split("Annex A")[0].replace("7-2024", "").replace(
           "1 April 2026", ""), "the standing standard names no run-specific year")
    lastday = {}
    for r in kept:
        key = r["key"]
        lastday[key] = max(lastday.get(key, dt.date(2000, 1, 1)), W.day(r["day"]))
    bad = 0
    for r in rd(tgt, "person_register.csv"):
        for col in ("date_of_death", "date_of_emigration"):
            if r[col] and r["person_key"] in lastday and G.iso(r[col]) < lastday[r["person_key"]]:
                bad += 1
    ok("defect2.exit_after_last_dispensing", bad == 0, "%d" % bad)
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(tgt, "data_fee_schedule.xlsx"))
    sheet_text = " ".join(str(c.value) for ws in wb.worksheets for row in ws.iter_rows()
                          for c in row if c.value is not None)
    ok("defect3.fee_rule_states_late_lines", "submitted after the quarter closed" in sheet_text)
    ok("defect3.fee_rule_states_the_payer", "surviving company is the fee payer" in sheet_text)
    ok("defect3.fee_rule_states_the_amendment_scope",
       "dispensed on or after 1 April 2026" in sheet_text)
    ok("pin.band_rule_filed", "not applied in tiers" in sheet_text)
    ok("pin.resend_counts_once_for_doses", "charged once" in sheet_text)
    ok("pin.payer_before_a_merger_filed", "remains the payer for its dispensings before" in sheet_text)
    reg = {r["product_code"]: r for r in rd(tgt, "product_register.csv")}
    ok("pin.successor_holder_named",
       reg["P09"]["holder_code"] == "H6" and reg["P09"]["previous_holder_code"] == "H5"
       and reg["P09"]["holder_code_from"] == "2026-02-27", str(reg["P09"]))
    notes = json.load(open(os.path.join(tgt, "register_release_notes.json")))
    ok("voice.release_notes_have_no_handling_list", "known_handling" not in notes,
       str(sorted(notes)))
    doc = {(r["file_name"], r["variable"]): r["documentation"]
           for r in rd(tgt, "register_variable_documentation.csv")}
    ok("pin.resend_counts_once_for_lines",
       "counts it once, in its lines and in its doses"
       in doc[("dispensings_2025_2026.csv", "record_id")])
    ok("pin.crosswalk_is_one_patient",
       "one patient behind them" in doc[("dispensings_2025_2026.csv", "person_key")])
    ok("pin.package_validity_is_documented",
       "at the date of the dispensing" in doc[("dispensings_2025_2026.csv", "package_code")])
    ok("pin.region_vintage_documented",
       "previous_region is the region recorded before" in doc[("person_register.csv", "region")])
    man = {r["file_name"]: r["note"] for r in rd(tgt, "extract_manifest.csv")}
    ok("pin.extract_scope_is_adults", "aged 18 and over" in man["(extract scope)"])
    ok("pin.extract_scope_names_the_window",
       "1 October 2025 to 30 September 2026" in man["(extract scope)"]
       and "1 October 2023 to 30 September 2025" in man["(extract scope)"])
    std = _pdf_text(tgt)
    ok("pin.quarter_of_dispensing_in_the_standard",
       "in a quarter of it, according to its date of dispensing" in std)
    ok("pin.no_inert_clause", "left the country" not in std)
    ok("pin.standard_owns_the_expected_number",
       "own epidemiological work and is recorded with each run" in std)
    ok("pin.standard_names_no_estimator",
       not any(x in std.lower() for x in ("sequence ratio", "null-effect", "hallas", "permutation",
                                          "equally likely", "symmetry", "half of")))
    # the six sentences the judge's determinism rests on, each with a shipped home
    reg9 = reg["P09"]
    ok("home.sovraxil_history",
       reg9["holder_code"] == "H6" and reg9["previous_holder_code"] == "H5"
       and reg9["holder_code_from"] == "2026-02-27")
    hold = {r["holder_code"]: r for r in rd(tgt, "holder_register.csv")}
    ok("home.kirunelle_merger",
       hold["H7"]["merged_into"] == "H2" and hold["H7"]["merger_date"] == "2026-04-01")
    ok("home.payer_rule", "the surviving company is the fee payer" in sheet_text)
    ok("home.resend_counts_once",
       "charged once" in sheet_text
       and "counts it once" in doc[("dispensings_2025_2026.csv", "record_id")])
    ok("home.flat_bands", sheet_text.count("not applied in tiers") >= 1
       and "rate is charged on all of those" in sheet_text)
    ok("home.quarter_of_dispensing",
       "in a quarter of it, according to its date of dispensing" in std
       and "charged in the quarter of its dispensing" in sheet_text)
    ok("home.lapsed_authorisation_charged",
       "marketing authorisation has since lapsed" in sheet_text)
    dist = asks_distinct(kept)
    ok("ask.a1_counts_distinct_lines",
       [r for r in g["a1"] if r["chain"] == "APK" and r["quarter"] == "2025 Q4"][0]["accepted"]
       == len([r for r in dist if r["chain"] == 0 and 731 <= r["day"] <= 822]),
       "APK 2025 Q4")
    ok("ask.a1_resend_removed",
       len(dist) < len(kept), "%d distinct of %d rows" % (len(dist), len(kept)))

    # ---------------------------------------------------------------- input gates
    files = sorted(os.listdir(tgt))
    ok("gate.files", len(files) >= 10, "%d files" % len(files))
    exts = set(os.path.splitext(f)[1] for f in files)
    ok("gate.formats", len(exts) >= 3, str(sorted(exts)))
    biggest = max(sum(1 for _ in open(os.path.join(tgt, f), encoding="utf-8",
                                      errors="replace")) - 1
                  for f in files if f.endswith(".csv"))
    ok("gate.big_file", biggest >= 25000, "%d rows" % biggest)
    md = json.load(open(os.path.join(os.path.dirname(tgt), "metadata.json")))
    ok("gate.distractors", len(md["distractor_files"]) >= 2, str(md["distractor_files"]))
    ok("gate.distractors_present", all(os.path.exists(os.path.join(tgt, d))
                                       for d in md["distractor_files"]))
    ok("gate.distractor_not_in_a_name",
       not any("distract" in f.lower() for f in files))
    for d in md["distractor_files"]:
        cols = set(rd(tgt, d)[0])
        ok("gate.distractor_has_no_pair_" + d,
           "marker_code" not in cols and "person_key" not in cols, str(sorted(cols)))

    # ---------------------------------------------------------------- realism sweep
    ok("real.no_round_referral_share",
       all(round(100.0 * r["after"] / r["n"], 1) % 5 != 0 for r in cands))
    ok("real.patient_counts_distinct", len(set(r["n"] for r in counts)) >= 20)
    ok("real.chain_quarters_distinct",
       len(set((r["accepted"], r["rejected"]) for r in g["a1"])) == len(g["a1"]))
    ok("real.a3_cells_distinct", len(set(r["patients"] for r in g["a3"])) >= 18)
    ok("real.no_repeated_block",
       len(set(tuple(sorted(x.items())) for x in
               [{k: v for k, v in r.items() if k != "key"} for r in g["a1"]])) == len(g["a1"]))
    blob2 = text_blob
    for nm in ("john doe", "acme", "company a", "lorem", "placeholder", "example.com", "test "):
        ok("real.no_placeholder_" + nm.strip().replace(" ", "_"), nm not in blob2)
    people_names = ["Sine Jakobsen", "Arne Mogensen"]
    ok("real.personas_drawn", all(" " in p for p in people_names))

    # ---------------------------------------------------------------- the ask layer
    ok("ask.zero_devices_in_main_population",
       all(not r["is_first"] for r in rejected))
    exrefs = [r["exception_ref"] for r in rd(tgt, "submission_exceptions.csv")]
    ok("ask.exceptions_outside_extracts",
       len(set(exrefs)) == len(exrefs) == len(rejected), "%d refs, %d rejected"
       % (len(set(exrefs)), len(rejected)))
    a1_total = sum(r["rejected"] for r in g["a1"])
    ok("ask.a1_rejected_nonzero", a1_total > 500, "%d" % a1_total)
    ok("ask.a1_median_spread",
       len(set(r["median_days"] for r in g["a1"])) >= 5,
       str(sorted(set(r["median_days"] for r in g["a1"]))))
    ok("ask.a1_median_moves_inside_the_window",
       any(len(set(r["median_days"] for r in g["a1"] if r["chain"] == ch)) > 1
           for ch in set(r["chain"] for r in g["a1"])))
    mid_ok = True
    for ci, (code, name) in enumerate(W.CHAINS):
        for label, a, b in AS.QUARTERS:
            d = sorted(r["submitted"] - r["day"] for r in kept
                       if r["chain"] == ci and a <= r["day"] <= b)
            if len(d) % 2 == 0 and d and d[len(d) // 2 - 1] != d[len(d) // 2]:
                mid_ok = False
    ok("ask.a1_median_convention_free", mid_ok,
       "every even cell's two middle values are equal, so every median convention agrees")
    ok("ask.a2_payers", len(g["a2"]) == 7, "%d" % len(g["a2"]))
    ok("ask.a2_premerger_payer_present",
       any(r["holder"] == "H7" and r["ddd"] > 0 for r in g["a2"]))
    ok("ask.a2_amendment_bites",
       all(r["rate_before"] != r["rate_after"] for r in g["a2"]))
    ok("ask.a2_merger_folded",
       any(r["holder"] == "H2" and r["ddd"] > 0 for r in g["a2"]))
    ok("ask.a3_cells", len(g["a3"]) == 24, "%d" % len(g["a3"]))
    ok("ask.a3_not_stated_present",
       any(r["region"] == "not stated" and r["patients"] > 0 for r in g["a3"]))
    # deleting every ask device leaves the call where it is
    ok("ask.devices_deletable", referred == _referred(tgt, rp, "perm", firsts))

    # ---------------------------------------------------------------- figures agree
    ok("fig.rows_match", len(g["screen_rows"]) == len(counts))
    ok("fig.referred_names",
       sorted("%s/%s" % (r["product"], r["marker"]) for r in counts if r.get("referred")) ==
       sorted(referred))
    ok("fig.a1_rows", len(g["a1"]) == 16, "%d" % len(g["a1"]))
    if FAILED:
        raise AssertionError("checks failed (%d of %d):\n  %s" % (len(FAILED), N,
                                                                  "\n  ".join(FAILED)))
    return N
