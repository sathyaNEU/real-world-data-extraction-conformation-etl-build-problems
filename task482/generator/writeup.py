"""submission.md from figures.json: the tags, the call, the critical components, the steps and the deliverable
answers, every figure emitted from the generator's own numbers."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def n(x):
    return "{:,}".format(x)


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    C, R, S = F["components"], F["rivals"], F["system"]
    ca, cca = F["call"]["college_algebra_score"], F["call"]["corequisite_score"]
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** Education & Learning Sciences (item response theory and test equating).")
    out.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    out.append("## 1. Final Recommendation\n")
    out.append("**Form 27A should place students into College Algebra from a raw score of %d and into Corequisite "
               "College Algebra from %d.**" % (ca, cca))
    out.append("A student at the College Algebra standard is expected to reach %.1f of the form's 60 scored items and "
               "a student at the Corequisite College Algebra standard %.1f, once each unique item is carried from the "
               "field-test section it was calibrated in to the positions it takes on Northgate Assess. Not %d and %d, "
               "the scores the bank difficulties give as filed (%.1f and %.1f), which hold every unique item as hard "
               "as it was at positions 61 to 70.\n" % (C["expected_raw_ca"], C["expected_raw_cca"], R["filed_ca_score"],
                                                       R["filed_cca_score"], R["filed_expected_ca"],
                                                       R["filed_expected_cca"]))
    out.append("## 2. Critical Components\n")
    out.append("1. Position term of the Rasch model fitted to the 2026 attempts, from the field-test section's mean position "
               "(65.5) to Form 27A's (45.5): **%.2f** logits" % C["carry_logits"])
    out.append("2. Expected raw score on Form 27A at the College Algebra standard (0.20 logits): **%.1f**"
               % C["expected_raw_ca"])
    out.append("3. Expected raw score on Form 27A at the Corequisite College Algebra standard (-0.70 logits): **%.1f**\n"
               % C["expected_raw_cca"])
    out.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Converted the Itemstore assembly pool's difficulties from bank units to logits (QPI-TR-2027 section 4) and "
        "took Form 27A's anchor block and 40 unique items from qpi_form_27A_assembly.csv.",
        "Scored every 2026 response: the Kestrel Testing Suite's response strings against the keys at their version's "
        "positions in qpi_forms_26A_26B_layout.csv, and Northgate Assess's item responses at their delivered seq.",
        "Fitted the Rasch model with a linear position term to all 2026 responses by marginal maximum likelihood, the "
        "anchor block fixed at its bank difficulties and every other item free: %.2f logits over the 20 positions "
        "from the field-test section's mean to Form 27A's." % C["carry_logits"],
        "Carried each unique item from the old platform's field-test section (mean position %.1f) to each of positions "
        "21 to 70 on Northgate Assess and averaged its expected score over the shuffle; the anchor block, calibrated "
        "in place, kept its bank difficulties." % C["field_test_mean_position"],
        "Summed the 60 expected scores at each standard: %.1f at College Algebra and %.1f at Corequisite College "
        "Algebra." % (C["expected_raw_ca"], C["expected_raw_cca"]),
        "Matched each student across both platforms and both student identifiers on birth date, sex, high school code "
        "and registration date, and left out the attempts in sessions qpi_session_review_log_2026.xlsx leaves "
        "invalidated.",
        "Placed each student on their higher level (the later sitting on a tie) at the college their placing sitting's "
        "automatic score report went to in qpi_score_reports_2026-03-01_to_2027-01-31.csv: %s students placed, %s "
        "into College Algebra and %s into Corequisite College Algebra, %s of them sat twice."
        % (n(S["placed"]), n(S["CA"]), n(S["CCA"]), n(S["twice"])),
        "Set the placement scores at the lowest whole raw scores at or above the expected raw scores (QPI-TR-2027 "
        "section 7): College Algebra from %d, Corequisite College Algebra from %d." % (ca, cca),
    ]
    for i, s in enumerate(steps):
        out.append("%d. %s" % (i + 1, s))
    out.append("\n## 4. Deliverable Answers\n")
    out.append("### qpi_placement_review_2027.xlsx\n")
    out.append("1. Placement scores: College Algebra %d, Corequisite College Algebra %d." % (ca, cca))
    out.append("2. Expected raw score at the standard: College Algebra %.1f, Corequisite College Algebra %.1f."
               % (C["expected_raw_ca"], C["expected_raw_cca"]))
    out.append("3. Each college from 1 March 2026 to 31 January 2027, whole students (placed; College Algebra; "
               "Corequisite College Algebra; sat twice):")
    for code in sorted(F["colleges"]):
        r = F["colleges"][code]
        out.append("   - %s %s: %s placed, %s College Algebra, %s Corequisite College Algebra, %s sat twice"
                   % (code, r["name"], n(r["placed"]), n(r["CA"]), n(r["CCA"]), n(r["twice"])))
    out.append("   - System: %s placed, %s College Algebra, %s Corequisite College Algebra, %s sat twice\n"
               % (n(S["placed"]), n(S["CA"]), n(S["CCA"]), n(S["twice"])))
    conv = F["conversion"]
    lo_cca = min(int(r) for r, v in conv.items() if v == "CCA")
    lo_ca = min(int(r) for r, v in conv.items() if v == "CA")
    out.append("### qpi_form27a_score_conversion.csv\n")
    out.append("4. Raw scores 0 to %d Developmental Mathematics (MATH 091), %d to %d Corequisite College Algebra (MATH "
               "131 with MATH 031), %d to 60 College Algebra (MATH 131).\n" % (lo_cca - 1, lo_cca, lo_ca - 1, lo_ca))
    out.append("### qpi_form27a_expected_score_curve.svg\n")
    out.append("5. Form 27A's expected raw score against ability in logits, the two standards marked (0.20 and -0.70) "
               "with their expected raw scores (%.1f and %.1f) and placement scores (%d and %d), and the curve from the "
               "bank difficulties as filed dashed." % (C["expected_raw_ca"], C["expected_raw_cca"], ca, cca))
    text = "\n".join(out) + "\n"
    assert "—" not in text and "–" not in text
    open(os.path.join(TASK, "submission.md"), "w", encoding="utf-8").write(text)
    return text


if __name__ == "__main__":
    print(main())
