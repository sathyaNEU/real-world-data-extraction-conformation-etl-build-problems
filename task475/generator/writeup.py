"""Writes submission.md from generator/figures.json: every figure in the write-up is one the generator computed.

    python3 task475/generator/writeup.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def signed(v):
    return "+%d" % v if v > 0 else ("%d" % v if v < 0 else "0")


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    mv = f["moves"]
    moves = ", ".join("%s %s" % (q, signed(mv[q])) for q in sorted(mv, key=lambda q: int(q[1:])))
    fm = f["facility_moves"]
    c = f["centres"]
    order = ["Sydney", "Western Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"]
    t = f["centre_totals"]
    lines = [
        "## Tags",
        "",
        "**Domain:** Education & Learning Sciences (item response theory and test equating: the optional questions "
        "of a written accreditation paper put on one mark scale when each candidate chooses which questions to "
        "answer).",
        "**Analytical objective:** Data Extraction & Conformation (ETL).",
        "",
        "## 1. Final Recommendation",
        "",
        "**Approve the November 2026 Paper 2 results with the optional questions moved %s marks: %d of the %d "
        "candidates who sat pass.** Not the moves set from each question's mean mark (Q6 %s, Q8 %s, %d passing): "
        "the stronger candidates chose Question 6 and the weaker chose Question 8, and the candidates who answered "
        "Question 6 averaged %.1f on their other answers against %.1f on it, while Question 8's averaged %.1f "
        "against %.1f. Not the unmoved marks (%d passing)." %
        (moves, f["passed"], f["sat"], signed(fm["Q6"]), signed(fm["Q8"]), f["facility_passed"],
         f["q6_choosers_other_mean"], f["q6_mean"], f["q8_choosers_other_mean"], f["q8_mean"], f["unmoved_passed"]),
        "",
        "## 2. Critical Components",
        "",
        "1. Each question's difficulty for the candidates who sat, from a candidate-plus-question fit of the "
        "November marks of record, set against the average question counted once and rounded: **%s**." % moves,
        "2. Candidates who sat Paper 2: **%d**; with the moves applied and held within 0 and 20, **%d** reach 50 "
        "and pass." % (f["sat"], f["passed"]),
        "3. The candidates who answered Question 6 average **%.1f** on their other answers and **%.1f** on Question "
        "6; Question 8's average **%.1f** and **%.1f**." %
        (f["q6_choosers_other_mean"], f["q6_mean"], f["q8_choosers_other_mean"], f["q8_mean"]),
        "",
        "## 3. Step-by-Step Solution",
        "",
        "1. Took the NOV26 rows of cae_marking_export_2026.csv and summed each candidate's part marks per question, "
        "the last mark entered for each part (regulation 11.2), a no-response part counting nothing: %d candidates "
        "sat." % f["sat"],
        "2. Fitted each mark as a candidate effect plus a question effect over every answer, set each question's "
        "effect against the average of the question effects and rounded to the nearest whole mark (regulation "
        "14.1): %s." % moves,
        "3. Applied each move to every answer to its question, held within 0 and 20 (regulation 14.2), summed and "
        "passed totals of 50 or more (regulation 12): %d pass and %d fail." % (f["passed"], f["failed"]),
        "4. For each centre's Paper 2 entries in cae_entries_nov2026.csv, counted as withdrawn the entries "
        "withdrawn by a request in portal_requests_nov2026.json received before 7 November, Sydney time (regulation "
        "17.1; submitted is UTC, and requests sent in the last week were actioned on 9 and 10 November), and as "
        "absent the other entries with no NOV26 marks (regulation 17.3): %d withdrawals and %d absentees in all." %
        (t["withdrawals"], t["absentees"]),
        "5. Matched each November sitter to cae_candidates_may2026.xlsx on member number where both carry one, "
        "otherwise on family name, first given name and date of birth, and kept May candidates with MAY26 marks in "
        "the export (regulation 2, marked present): %d had sat Paper 2 in May." % t["may_sitters"],
        "6. Resolved each request in results_review_requests_2026.csv to its May candidate by candidate number and "
        "family name (%d numbers keyed with two digits transposed) and compared the result on the marks of record "
        "at issue on 30 June with the result after review, both with the minutes' May moves: %d results changed, "
        "each from fail to pass." % (f["reviews_rekeyed"], f["reviews_changed"]),
        "7. Refunded under regulation 19.4 the fees of those %d reviews and of the %d requests received after 21 "
        "July; card fees as paid, account fees at Schedule 1's fee for the day received less the firm's discount in "
        "corporate_accounts.csv (each account line repeats its invoice total): AUD %s." %
        (f["reviews_changed"], f["reviews_declined"], "{:,}".format(f["refund_aud"])),
        "8. Recommend approving the moves and the %d passes." % f["passed"],
        "",
        "## 4. Deliverable Answers",
        "",
        "### nov2026_paper2_results.csv",
        "",
        "1. One row for each of the %d candidates who sat, with the moved mark counted on each question answered, "
        "the total and Pass or Fail: %d Pass, %d Fail." % (f["sat"], f["passed"], f["failed"]),
        "",
        "### paper2_results_committee_paper.docx",
        "",
        "1. Moves, whole marks: %s." % moves,
        "2. Number passing: %d of %d." % (f["passed"], f["sat"]),
        "3. Bar chart of the moves by question (Figure 1, section 2).",
        "4. By centre, withdrawals, absentees and sitters who had also sat Paper 2 in May:",
    ]
    for nm in order:
        lines.append("   - %s: %d, %d, %d" % (nm, c[nm]["withdrawals"], c[nm]["absentees"], c[nm]["may_sitters"]))
    lines += [
        "5. May results changed on review: yes, %d, each from fail to pass." % f["reviews_changed"],
        "6. Review fees to refund: AUD %s." % "{:,}".format(f["refund_aud"]),
        "",
    ]
    with open(os.path.join(TASK, "submission.md"), "w") as fh:
        fh.write("\n".join(lines))


if __name__ == "__main__":
    main()
