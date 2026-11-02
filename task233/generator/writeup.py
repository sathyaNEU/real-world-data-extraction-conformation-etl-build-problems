"""submission.md, drafted from figures.json and the analysis results so no figure is typed."""
import json
import os


def andlist(xs):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def write(task_dir, res, fig):
    p = res["pack"]
    c, k = fig["call"], fig["components"]
    words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}
    dflt = p.outcomes(p.agreement())
    up = sum(1 for r in p.regions if res["outcomes"][r] == "Compliant" and dflt[r] == "Corrective action")
    cr = sum(1 for r in p.regions if res["outcomes"][r] == "Corrective action" and dflt[r] == "Service credit")
    cred = c["service_credit"]
    corr = c["corrective_action"]
    lines = []
    lines += ["## Tags", "",
              "**Domain:** Survey Research & Official Statistics, nonresponse, calibration and measurement-error adjustment (price collection quality assurance).",
              "**Analytical objective:** Data Quality Monitoring & Alerting.", ""]
    lines += ["## 1. Final Recommendation", "",
              "**Place %s under corrective action, put %s on a $%s service credit with corrective action, and assess the other %s regions as compliant.** "
              "%s is the only region whose estimated collection accuracy falls below the %s per cent band, and %s more fall short of %s per cent. "
              "Not the raw agreement between collector and Field Quality Team prices, which counts every price an outlet changed between the visit and the "
              "re-collection days later as a collector's error and would put %s compliant regions under corrective action and %s corrective regions on credits ($%s)."
              % (andlist(corr), andlist(cred), c["credit_dollars"], words[c["compliant_count"]], cred[0],
                 k["band_credit"], words[len(corr)], k["band_compliant"], words[up], words[cr], k["default_credit_dollars"]), ""]
    lines += ["## 2. Critical Components", "",
              "1. The Field Quality Team re-collected **%s** prices it found on the shelf; the share whose re-collected price differs from the collector's runs from **%s per cent** in %s to **%s per cent** in %s."
              % (k["prices_rechecked_found"], k["disagreement_low"], k["disagreement_low_region"], k["disagreement_high"], k["disagreement_high_region"]),
              "2. Net of the chance that each item's shelf price changed between the visit and its re-collection, %s's collection accuracy is the only one below **%s per cent**, and %s sit between %s and **%s per cent**; every other region is at %s per cent or more."
              % (cred[0], k["band_credit"], andlist(corr), k["band_credit"], k["band_compliant"], k["band_compliant"]),
              "3. The service credit is %s per cent of %s's quarterly collection fee of $%s: **$%s**."
              % (c["credit_percent"], cred[0], c["credit_regions_fee"][cred[0]], c["credit_dollars"]), ""]
    lines += ["## 3. Step-by-Step Solution", "",
              "1. Read pcqs_price_collection_quality_standard_v3.pdf: accuracy is the share of recorded prices that were the shelf price when the collector recorded it, estimated from the back-checks and set against %s and %s per cent without rounding (sections 3 and 4)."
              % (k["band_compliant"], k["band_credit"]),
              "2. Took the back-checked prices the officer found from the three monthly sheets of fqt_backcheck_register_2026q3.xlsx (%s prices) and compared each collector price with the FQT price." % k["prices_rechecked_found"],
              "3. Dated each collector's visit from tallis_visit_log_2026-07_2026-09.csv (the local date of started), joined through cpi_outlet_register_2026-10.xlsx (outlet code to contractor outlet no.), and took each back-check's delay in calendar days to its Re-collected on date.",
              "4. From cpi_field_quotes_2025-10_2026-09.csv, one row per quote and month with statuses read through handheld_status_codes.csv, took each COICOP class's monthly frequency of price change at multiples and at independents (outlet type in the register) over consecutive months priced on the same variety.",
              "5. Gave each back-check its chance of no shelf-price change, (1 minus that frequency) to the power delay/%s, and estimated each region's accuracy as its agreeing back-checks over the sum of those chances." % k["days_per_month"],
              "6. Applied section 4 and pcsa_schedule4_collection_fees.pdf: %s service credit of $%s, %s corrective action, the other regions compliant." % (cred[0], c["credit_dollars"], andlist(corr)),
              "7. Timeliness and missed visits: took the scheduled visits in tallis_collection_schedule_2026q3.csv, followed each Lifeline Chemists branch closed on 31 July to the CareMed Pharmacy outlet in the register at the same address (its quotes continue there in the price database), and counted a visit completed when every visit row with prices for the outlet in the month fell from the index day to the fourth working day after it in nso_collection_calendar_2026.csv (17 August a holiday); a schedule row with no visit row is a missed visit.",
              "8. Replacement acceptance: took the quarter's replacement rows (status R or 30) from the price database, kept one row per replacement where a quote was exported twice for the same visit, gave each decision in commodity_replacement_decisions_2026.xlsx to the latest replacement of its quote visited before the decision date, and counted a replacement accepted when its latest Comparable or Not comparable decision is Comparable.", ""]
    lines += ["## 4. Deliverable Answers", "", "### pcqs_2026q3_assessment.xlsx", "",
              "1. One row per region, outcome, timeliness (per cent), missed visits and replacement acceptance (per cent):"]
    for r in p.regions:
        d = fig["deliverables"][r]
        lines.append("   - %s %s: %s, timeliness %s, missed visits %d, replacement acceptance %s"
                     % (r, d["region"], d["outcome"], d["timeliness"], d["missed_visits"], d["replacement_acceptance"]))
    lines.append("2. Service credit for the quarter: $%s." % c["credit_dollars"])
    lines += ["", "### pcqs_2026q3_contractor_letter.pdf", "",
              "1. Outcomes: corrective action for %s; service credit and corrective action for %s; the other %s regions compliant."
              % (andlist(corr), andlist(cred), words[c["compliant_count"]]),
              "2. Service credit: $%s." % c["credit_dollars"],
              "3. Chart on page 1: a horizontal bar for each region's estimated collection accuracy, coloured by outcome, with the %s and %s per cent bands marked."
              % (k["band_compliant"], k["band_credit"]), ""]
    with open(os.path.join(task_dir, "submission.md"), "w") as f:
        f.write("\n".join(lines))
