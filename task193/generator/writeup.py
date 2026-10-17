"""task193: submission.md, drafted from the figures the generator emitted."""
import os


def f1(x):
    return ("%.1f" % x)


def write(task, g):
    L = []
    A = L.append
    A("# task193 submission")
    A("")
    A("## Tags")
    A("")
    A("**Domain:** Pharmacology, pharmacoepidemiology and safety (safety signal detection).")
    A("**Analytical objective:** Anomaly detection and diagnostics.")
    A("")
    A("## 1. Final Recommendation")
    A("")
    A("**Refer %d of the %d candidate pairs to formal signal assessment in the quarter beginning "
      "1 January 2027: %s.**" % (g["referred_count"], g["candidate_count"],
                                 "; ".join("%s and %s" % (r["product"], r["marker"])
                                           for r in g["referred"])))
    A("The expected after-count comes from the window's own first-receipt dates, so the lowest "
      "referred multiple is %.2f and the nearest pair on the wrong side of the line is %s at %.2f. "
      "Not the %d pairs an equal-chance expectation refers: it adds %s, which the dates refuse. "
      "And it misses %s, which are real signals it hides because both products were first marketed "
      "inside the window."
      % (min(r["multiple"] for r in g["referred"]), g["nearest_miss"]["label"],
         g["nearest_miss"]["multiple"], g["crude_count"],
         "; ".join("%s and %s" % (r["product"], r["marker"]) for r in g["crude_only"]),
         "; ".join("%s and %s" % (r["product"], r["marker"]) for r in g["window_only"])))
    A("")
    A("## 2. Critical Components")
    A("")
    A("1. The screen's candidate pairs are **%d** of the %d pairs in Annexes A and B"
      % (g["candidate_count"], g["screened_count"]))
    A("2. The pairs referred are **%d**" % g["referred_count"])
    A("3. The pairs an equal-chance expectation refers are **%d**" % g["crude_count"])
    A("4. The pairs it refers that this run does not are **%d**, and the pairs it hides are **%d**"
      % (len(g["crude_only"]), len(g["window_only"])))
    A("")
    A("## 3. Step-by-Step Solution")
    A("")
    A("1. Stacked dispensings_2023_2025.csv and dispensings_2025_2026.csv on the layouts "
      "register_release_notes.json gives and counted a re-sent line once, as those notes require: "
      "%d person keys appear across the extract." % g["patients_in_extract"])
    A("2. Folded the retired person keys in person_key_crosswalk.csv onto their current keys and "
      "mapped each package code to its treatment through package_index.csv at the date of the "
      "dispensing, per section 2.4.")
    A("3. Took each patient's earliest dispensing in each treatment as the first receipt and "
      "dropped first receipts falling in the clearance period, per sections 2.2 and 2.3.")
    A("4. Built each pair in screen_annexes.csv from the patients whose two first receipts both "
      "fall in the screen window and not on the same day, per section 2.5: %d of the %d pairs have "
      "at least 25 patients." % (g["candidate_count"], g["screened_count"]))
    A("5. Took the number expected if the product had no bearing on when the marker treatment is "
      "first received from the pair's own first-receipt dates, which the window makes unequal "
      "because two products were first marketed inside it and two lose their authorisation inside "
      "it.")
    A("6. Applied section 3.2: %d pairs reach 1.25 times that expected number and none of them is "
      "under assessment in signal_tracker_export.csv." % g["referred_count"])
    A("7. Compared with an equal-chance expectation, which refers %d pairs: %d of them fall below "
      "the line here and %d pairs below its line clear this one."
      % (g["crude_count"], len(g["crude_only"]), len(g["window_only"])))
    A("8. Refer the %d pairs for assessment in the quarter beginning 1 January 2027."
      % g["referred_count"])
    A("")
    A("## 4. Deliverable Answers")
    A("")
    A("### sequence_screen_2027Q1.xlsx")
    A("")
    A("1. The %d screened pairs in the order of the screen sheet, with the pair's patients, the "
      "patients in whom the marker treatment came after the product, the patients in whom it came "
      "before, and the referral:" % g["screened_count"])
    for r in g["screen_rows"]:
        if r["multiple"] is None:
            A("   - %s and %s: %d patients, %d after, %d before, below the 25-patient minimum"
              % (r["brand"], r["marker_treatment"], r["patients"], r["after"], r["before"]))
        else:
            A("   - %s and %s: %d patients, %d after, %d before, referred %s"
              % (r["brand"], r["marker_treatment"], r["patients"], r["after"], r["before"],
                 r["referred"]))
    # The nearest unreferred pair is not graded: the prompt asks for no such figure, and a graded
    # figure with no asking sentence has nothing to fix its basis or its population.
    A("2. Pairs referred: %d." % g["referred_count"])
    A("3. Lines accepted, lines rejected and median days from dispensing to submission, by chain "
      "and quarter of dispensing, whole counts and days to one decimal:")
    for r in g["a1"]:
        A("   - %s, %s: %d accepted, %d rejected, %s days"
          % (r["chain"], r["quarter"], r["accepted"], r["rejected"], f1(r["median_days"])))
    A("4. Defined daily doses dispensed in the screen window and the data fee due, by fee payer, "
      "doses to one decimal and fees to the nearest krone:")
    for r in g["a2"]:
        A("   - %s (%s): %s DDD, %d kroner" % (r["name"], r["holder"], f1(r["ddd"]), r["fee_dkk"]))
    A("5. Patients with a first receipt of a screened product in the window and the share of them "
      "with a first marker-treatment receipt in it, by region and age band at 1 October 2025, "
      "shares to one decimal:")
    for r in g["a3"]:
        A("   - %s, %s: %d patients, %s per cent"
          % (r["region"], r["band"], r["patients"], f1(r["share_pct"])))
    A("")
    A("### order_shares_by_pair.png")
    A("")
    first, last = g["chart_rows"][0], g["chart_rows"][-1]
    A("1. One horizontal bar for each of the %d screened pairs for the share of its patients "
      "who received the marker treatment after the product, with the %d referred pairs in the "
      "darker fill and the other %d in the lighter one."
      % (g["screened_count"], g["referred_count"],
         g["screened_count"] - g["referred_count"]))
    A("2. The bars run longest share first, from %s at %s per cent to %s at %s per cent."
      % (first["label"], f1(first["share_pct"]), last["label"], f1(last["share_pct"])))
    A("3. Title states that %d of the %d candidate pairs clear the referral line."
      % (g["referred_count"], g["candidate_count"]))
    A("")
    with open(os.path.join(task, "submission.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
