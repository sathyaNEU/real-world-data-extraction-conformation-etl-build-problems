"""submission.md, metadata.json and prompt.txt, from the golden figures."""
import json
import os

import golden as G

QN = {"Q1": "October to December 2025", "Q2": "January to March 2026", "Q3": "April to June 2026",
      "Q4": "July to September 2026"}
QE = {"Q1": "2025-12-31", "Q2": "2026-03-31", "Q3": "2026-06-30", "Q4": "2026-09-30"}
DISTRACTORS = ["aov_2024-25_published_extract.pdf", "larkspur_100_factsheet_sep2026.pdf"]

PROMPT = ("How big was the Thornbury Managed Risk UK Equity Fund's 2025-26 shortfall against its benchmark, which change "
          "on the board's list would have removed the most of it, and how much would each change have removed? Alongside "
          "that pricing, change_pricing_2025-26.xlsx needs each sleeve's dividend income for each quarter of the "
          "accounting year by ex-dividend date, counting only dividends paid or still to be paid, in cash or in new "
          "shares; each sleeve's commission and stamp duty for each quarter by the date of the trade; and, at each "
          "quarter-end, how many of the growth sleeve's holdings at the custodian were quoted on AIM and their share of "
          "the sleeve at the custodian's prices. The change, the runner-up and a chart of every change's figure go in "
          "board_review_2025-26.pptx. The shortfall and the changes are in basis points to the nearest 10, income to "
          "the nearest 1,000 pounds, dealing costs to the nearest 100 pounds and AIM shares in per cent to one decimal.")


def gbp(x):
    return "{:,}".format(int(x))


def dfmt(d):
    return d.isoformat()


def write_all(task, target, S, Fg):
    M, f = Fg["M"], Fg["figs"]
    c, ru = M["call"], M["runner_up"]
    nm = {"A": "running the value sleeve as a tracker", "B": "running the growth sleeve as a tracker",
          "C": "raising the overlay's trigger to 12%", "D": "restoring full exposure within 6%",
          "E": "equitising the liquidity sleeve"}
    ep = M["ep_actual"][0]
    last_reduced = G.DAYS[G.IDX[ep[1]] - 1]
    lines = []
    lines += ["## Tags", "", "**Domain:** Quantitative finance (factor and return attribution).",
              "**Analytical objective:** Root-cause analysis.", ""]
    lines += ["## 1. Final Recommendation", "",
              "**Run the value sleeve as a tracker of the benchmark: replayed on 2025-26 it removes %d bp of the B "
              "Accumulation shares' %d bp shortfall against the Larkspur UK All-Share, %d bp more than the runner-up, "
              "raising the overlay's trigger to 12%% (%d bp).** Not the higher trigger, which the year's attribution and "
              "any replay that keeps the overlay's recorded exposure put first: Penrose Bank's collapse in the value "
              "sleeve is what took the B Accumulation price more than 8%% below its 63-day high on %s, and with the "
              "sleeve tracking the benchmark the price's deepest fall below its high is %.1f%%, short of the 8%% line, so the overlay never "
              "cuts exposure and the fund keeps the April to June rebound."
              % (f["bp_" + c], f["short_bp"], f["gap_bp"], f["bp_" + ru], dfmt(M["trigger_day"]), f["A_worst_pct"]), ""]
    lines += ["## 2. Critical Components", "",
              "1. Over the accounting year (from the noon valuation point on 2025-09-30 to the one on 2026-09-30) the B "
              "Accumulation shares returned **%.1f%%** and the benchmark at the valuation point **%.1f%%**: a shortfall "
              "of **%d bp**." % (f["R_bacc_pct"], f["R_bench_pct"], f["short_bp"]),
              "2. As the year ran, the B Accumulation price closed **%.1f%%** below its 63-day high on %s and the overlay "
              "held equity exposure at 40%% from %s to %s." % (f["dd_trigger_pct"], dfmt(M["trigger_day"]),
                                                               dfmt(ep[0]), dfmt(last_reduced)),
              "3. Each change replayed with the overlay rule run on that fund's own price removes: value sleeve as a "
              "tracker **%d bp**, higher trigger **%d bp**, earlier restoration **%d bp**, growth sleeve as a tracker "
              "**%d bp**, equitised liquidity sleeve **%d bp**." % (f["bp_A"], f["bp_C"], f["bp_D"], f["bp_B"], f["bp_E"]),
              "4. With the value sleeve as a tracker the price's deepest fall below its high is **%.1f%%** (%s) and exposure is "
              "never reduced; the gap to the runner-up is **%d bp**." % (f["A_worst_pct"], dfmt(M["A_worst_day"]),
                                                                       f["gap_bp"]), ""]
    lines += ["## 3. Step-by-Step Solution", "",
              "1. Took each sleeve's daily return from thornbury_mruke_valuation_summary.csv (each valuation over the "
              "previous one plus its quarter-end transfer), the benchmark's noon total return from "
              "larkspur_index_levels_2025-26.csv, the liquidity fund's yield, and the contracts and noon futures marks "
              "from merrow_overlay_daily_monitor_2025-26.xlsx.",
              "2. Rebuilt the fund at each valuation point as the prospectus runs it (dealing, charges by class, "
              "distributions and futures margin through the liquidity sleeve; the 47/47/6 rebalance at each "
              "quarter-end), reproducing the published B Accumulation price.",
              "3. For each change on the review terms' list, swapped the sleeve's return for the benchmark's or changed "
              "the rule's line, and ran the overlay rule on that fund's own B Accumulation price from 2025-09-30 "
              "(63 valuation points, more than 8% below to reduce, within 4% to restore, both from the next dealing "
              "day, 40% exposure in whole contracts).",
              "4. Priced each change as its replayed B Accumulation return less the return as it ran, and ranked them.",
              "5. Dividend income: holloway_income_entitlements_2025-26.csv for ex-dates to 2026-03-31 without Penrose "
              "Bank's March final (never paid after its resolution), plus the scrip-alternative dividends that report "
              "omits; Northcote receipts and scrip shares dated by their ex-dates in corporate_actions_feed_20261016.csv; "
              "dividends unpaid at the extract's end (2026-10-16) from the settled holding on the record date.",
              "6. Dealing costs: commission plus stamp duty, each trade dated two UK dealing days before settlement "
              "(trades of 2025-12-31 settled on 2026-01-05), with the trades open at the change of custodian "
              "taken once from holloway_open_trades_31mar2026.csv.",
              "7. AIM holdings: the growth sleeve's settled holdings at each quarter-end at the custodian's close prices, "
              "with each company's market as at that date (two moved from AIM to the Main Market, on 2026-05-18 and "
              "2026-09-07).", ""]
    lines += ["## 4. Deliverable Answers", "", "### change_pricing_2025-26.xlsx", "",
              "1. Shortfall removed by each change (bp): value sleeve as a tracker %d; higher trigger %d; earlier "
              "restoration %d; growth sleeve as a tracker %d; equitised liquidity sleeve %d. Shortfall %d bp."
              % (f["bp_A"], f["bp_C"], f["bp_D"], f["bp_B"], f["bp_E"], f["short_bp"]),
              "2. Dividend income by ex-dividend date (GBP):"]
    for tag, sl in (("V", "Value sleeve"), ("G", "Growth sleeve")):
        lines.append("   - %s: %s" % (sl, "; ".join("%s %s" % (QN[q], gbp(f["inc_%s_%s" % (tag, q)]))
                                                   for q in ("Q1", "Q2", "Q3", "Q4"))))
    lines.append("3. Commission and stamp duty by quarter of trade (GBP):")
    for tag, sl in (("V", "Value sleeve"), ("G", "Growth sleeve")):
        lines.append("   - %s: %s" % (sl, "; ".join("%s %s" % (QN[q], gbp(f["cost_%s_%s" % (tag, q)]))
                                                   for q in ("Q1", "Q2", "Q3", "Q4"))))
    lines.append("4. Growth sleeve holdings quoted on AIM: %s." % "; ".join(
        "%s %d holdings, %.1f%%" % (QE[q], f["aim_n_" + q], f["aim_pct_" + q]) for q in ("Q1", "Q2", "Q3", "Q4")))
    lines += ["", "### board_review_2025-26.pptx", "",
              "1. The change: run the value sleeve as a tracker of the benchmark, %d bp of the shortfall removed."
              % f["bp_" + c],
              "2. Runner-up: raise the overlay's trigger to 12%%, %d bp; difference %d bp." % (f["bp_" + ru], f["gap_bp"]),
              "3. Bar chart of every change's figure in basis points on slide 2.", ""]
    with open(os.path.join(task, "submission.md"), "w") as fh:
        fh.write("\n".join(lines))
    with open(os.path.join(task, "prompt.txt"), "w") as fh:
        fh.write(PROMPT)
    meta = dict(task="task398",
                decision="which one change on the board's list the authorised fund manager makes to the Thornbury "
                         "Managed Risk UK Equity Fund for 2026-27, priced as the 2025-26 shortfall it would have removed",
                deliverables=["change_pricing_2025-26.xlsx", "board_review_2025-26.pptx"],
                distractor_files=["target/" + x for x in DISTRACTORS],
                files={})
    for fn in sorted(os.listdir(target)):
        meta["files"]["target/" + fn] = dict(
            source="synthetic, generated by task398/generator from seed 398 (an invented fund, index provider and "
                   "organisations)", date="2026-11-03", licence="CC BY 4.0")
    with open(os.path.join(task, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=1)
