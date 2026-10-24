"""submission.md, every figure read from generator/figures.json."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def usd(v):
    return "USD {:,.2f}".format(v)


def hrs(v):
    return ("%.1f" % v).rstrip("0").rstrip(".") if v != int(v) else "%d" % v


def write(fig_path, out_path):
    f = json.load(open(fig_path))
    ds = f["districts"]
    order = sorted(ds, key=lambda k: (ds[k]["state"], ds[k]["name"]))
    owed = [k for k in order if ds[k]["result"] == "Not met"]
    o = ["## Tags\n",
         "**Domain:** Education & Learning Sciences, item response theory and test equating (an education technology "
         "company's partner district contracts, its platform's eligibility and roster records, the assessment delivery "
         "system's sessions and scored responses, the contractor's item parameters and plausible values, the "
         "professional learning scheduling export and the billing register conformed into the 2025-26 guarantee "
         "settlement and the billing system's credit memo import).",
         "**Analytical objective:** Data Extraction & Conformation (ETL).\n",
         "## 1. Final Recommendation\n",
         "**%d of the 58 partner districts are owed the outcomes guarantee credit under their 2025-26 order forms, "
         "%s in total: %s.**" % (len(owed), usd(f["call"]["og_total"]),
                                 "; ".join("%s (%s)" % (ds[k]["name"], k) for k in owed)),
         "Each district's Outcome Share is estimated from its eligible students' own answers on the two modules they "
         "took, with the district in the population model. The contractor's plausible values were drawn for the "
         "national report from a model on grade, state, prior band and background with no district term, so they pull "
         "every district toward what its students' backgrounds predict: averaged by district they credit districts "
         "that met their benchmark and clear districts that did not.\n",
         "## 2. Critical Components\n",
         "1. Districts owed the outcomes credit: **%d** of 58." % len(owed),
         "2. Outcomes credits: **%s** in total." % usd(f["call"]["og_total"]),
         "3. Professional learning shortfall credits: **%s** across **%d** districts; all credits **%s**.\n"
         % (usd(f["pl_total"]), f["n_pl"], usd(f["credit_total"])),
         "## 3. Step-by-Step Solution\n",
         "1. Took each district's eligible students from guarantee_eligibility_2025_26.csv (the 1 May 2026 record "
         "flagged eligible) and linked them through student_id_crosswalk_2025_26.csv to their submitted session in "
         "lsoa_spring2026_sessions.csv: %s eligible students assessed." % "{:,}".format(sum(ds[k]["assessed"] for k in order)),
         "2. Scored each submitted session's responses (omitted items incorrect, items not reached left out) on the "
         "2024 item parameters, two-parameter logistic with D = 1.",
         "3. Fitted a latent regression of achievement on district, grade, prior state-test band (Table 5 of the "
         "technical report, read from the roster uploads) and the three status flags by EM on a grid, and took each "
         "district's Outcome Share as the mean posterior probability of its eligible assessed students being at or "
         "above 500, 520 or 540 for their grade.",
         "4. Compared each share with the district's Guarantee Benchmark in order_forms_2025_26.xlsx; a district below "
         "it is credited its Credit Percentage of the 2025-26 Subscription Fee.",
         "5. Summed each district's live sessions (virtual live and on site) in pd_sessions_2025_26.csv with status "
         "Delivered and a date in its subscription term, each session's hours read as hours and minutes after the "
         "point (the scheduling system's way of writing a session's time), joint sessions in full for every district "
         "attending, to the nearest half hour; any shortfall against the order form's hours is credited at USD 250 an "
         "hour under the agreement's professional learning clause.",
         "6. Applied each credit to the open 2026-27 subscription invoice on the order form's bill-to account with the "
         "earliest due date in billing_invoices_2026_27.csv, or a refund by check where none is open, in the layout of "
         "credit_memo_import_layout.pdf.\n",
         "## 4. Deliverable Answers\n",
         "### lumenfold_guarantee_settlement_2025_26.xlsx\n",
         "1. Outcomes guarantee: not met, and credited, at the %d districts in the Final Recommendation; met at the "
         "other %d." % (len(owed), len(order) - len(owed))]
    o.append("2. Live professional learning hours delivered in the subscription term, to the half hour, against the "
             "order form's hours:")
    for k in order:
        o.append("   - %s (%s): %s of %s" % (ds[k]["name"], k, hrs(ds[k]["pd_delivered"]), hrs(ds[k]["pd_contract"])))
    o.append("3. Professional learning shortfall credit, USD to the cent (every other district nil):")
    for k in order:
        if ds[k]["pl"] > 0:
            o.append("   - %s (%s): %s" % (ds[k]["name"], k, usd(ds[k]["pl"])))
    o.append("\n### guarantee_credit_memos_2026.csv\n")
    o.append("4. %d credit memos dated 2026-11-30 (memo reference, customer account, reason, amount, applied to):"
             % len(f["memos"]))
    for m in f["memos"]:
        o.append("   - %s, %s, %s, %s, %s" % (m["memo_reference"], m["customer_account"], m["reason_code"],
                                              "%.2f" % m["credit_amount"],
                                              m["apply_to_invoice"] if m["refund_method"] == "APPLY" else "CHECK"))
    open(out_path, "w").write("\n".join(o) + "\n")


if __name__ == "__main__":
    write(os.path.join(HERE, "figures.json"), os.path.join(os.path.dirname(HERE), "submission.md"))
