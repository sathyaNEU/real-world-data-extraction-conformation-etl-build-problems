"""submission.md, written from figures.json so every figure it states is one the generator computed."""
import datetime as dt
import json

CATS = ["Womenswear", "Menswear", "Footwear", "Home", "Kids", "Accessories"]


def c(n):
    return "{:,}".format(n)


def mname(k):
    return dt.date(int(k[:4]), int(k[5:]), 1).strftime("%B")


def write(fig_path, out_path):
    f = json.load(open(fig_path))
    months = sorted(f["months"])
    m = f["months"]
    breach = [mname(k) for k in f["breach_months"]]
    btxt = ", ".join(breach[:-1]) + " and " + breach[-1]
    r1, r3, r0 = f["rungs"]["r1_arrival_order"], f["rungs"]["r3_random_order"], f["rungs"]["r0_opened_as_delivered"]
    b1 = [mname(k) for k in r1["breach_months"]]
    lb, bt = f["labels"], f["backtest_2025"]
    late_list = ", ".join(c(m[k]["refunds_late"]) for k in months[:-1]) + " and " + c(m[months[-1]]["refunds_late"])
    share_list = ", ".join("%.1f" % m[k]["late_share_pct"] for k in months[:-1]) + " and " + \
        "%.1f" % m[months[-1]]["late_share_pct"]
    s = []
    s.append("## Tags\n")
    s.append("**Domain:** General Statistics & Data Science (data integration, record linkage and entity resolution).")
    s.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    s.append("## 1. Final Recommendation\n")
    s.append("**Wrenfield & Holt should pay GBP %s into the customer goodwill fund for the %s refunds it made late in "
             "January to June 2026, and report %s as the months that broke the 95 per cent commitment.**" %
             (c(f["payment_gbp"]), c(f["late_total"]), btxt))
    s.append("Each refund's delivery day comes from replaying the goods-in scans and the openings in the order the "
             "centre works its hall, the newest parcel waiting opened first, the order every labelled opening shows "
             "(%s of %s). Not GBP %s with %s only, which pairing the two records in arrival order gives: that order "
             "matches %s of the labelled openings and finds none of 2025's late refunds. Not GBP %s, which treating "
             "every waiting parcel as equally likely gives. Not GBP %s, which reading the opening day as the delivery "
             "day gives." % (c(lb["newest_exact"]), c(lb["labelled_openings"]), c(r1["payment_gbp"]),
                             " and ".join(b1), c(lb["arrival_exact"]), c(r3["payment_gbp"]), c(r0["payment_gbp"])))
    s.append("\n## 2. Critical Components\n")
    s.append("1. The newest parcel waiting is the one opened on **%s** of **%s** labelled openings (every opening to "
             "the end of 2025 and the labelled stragglers opened to April 2026); arrival order matches **%s**." % (
                 c(lb["newest_exact"]), c(lb["labelled_openings"]),
                                                     c(lb["arrival_exact"])))
    s.append("2. Replayed that way, 2025's labelled late refunds are reproduced: **%s** in February and **%s** in "
             "December, both of which arrival order puts at **%s**." % (c(bt["labels"]["2"]), c(bt["labels"]["12"]),
                                                                       c(bt["arrival"]["2"])))
    s.append("3. Refunds made late, January to June 2026: **%s** (shares **%s** per cent of each month's refunds)." %
             (late_list, share_list))
    s.append("\n## 3. Step-by-Step Solution\n")
    s.append("1. Took the return's definitions from paragraphs 2 to 5 of calvermoor_written_assurance_oct2026.pdf: "
             "return refunds made in each month, made late on day 15 or later counting calendar days from the goods-in "
             "scan day, GBP %d a late refund, %d per cent made by day 14 each month." %
             (f["payment_per_late_gbp"], f["commitment_pct"]))
    s.append("2. Joined cotterby_goods_in_2025.csv and cotterby_goods_in_2026.parquet into one UK-time record of return "
             "parcels delivered, and dated each return refund from wh_refund_ledger_2025_2026.parquet at its PAID row "
             "(a failed card refund at its store-credit reissue): %s refunds made in January to June 2026." %
             c(f["refunds_total"]))
    s.append("3. Tested the pairing of deliveries to openings on the openings in "
             "cotterby_returns_processing_2025_2026.csv that carry the parcel's prepaid label (every opening to the "
             "end of 2025 and the labelled stragglers opened to April 2026): newest-first matches %s of %s, "
             "arrival order %s." % (c(lb["newest_exact"]), c(lb["labelled_openings"]), c(lb["arrival_exact"])))
    s.append("4. Replayed every delivery and opening from 2 December 2024 in time order, each opening (rejected parcels "
             "included) taking the newest parcel waiting, which reproduces 2025's labelled late refunds (%s in "
             "February, %s in December)." % (c(bt["labels"]["2"]), c(bt["labels"]["12"])))
    s.append("5. Counted each 2026 month's refunds made on day 15 or later from their parcel's delivery day: %s in all, "
             "with more than 5 per cent late in %s; the payment is %s refunds at GBP %d, GBP %s." %
             (c(f["late_total"]), btxt, c(f["late_total"]), f["payment_per_late_gbp"], c(f["payment_gbp"])))
    s.append("6. Valued every voucher in wh_goodwill_vouchers_2026.csv in pounds by its UK issue month, reading each "
             "customer's currency from wh_orders_returning_customers.parquet and converting euros at the extract's "
             "reporting rate of %.2f (a euro voucher is redeemed on euro orders in wh_voucher_redemptions_2026.csv)."
             % f["eur_rate"])
    s.append("7. Counted and valued every Refund delay voucher issued in January to June by the main category of the "
             "order named in the case it was issued on (wh_customer_cases_2026.csv), not the voucher's own order "
             "field, which for some vouchers names a later order of the customer's that was never returned or "
             "refunded.")
    s.append("8. Recommendation: pay GBP %s and report %s as breach months." % (c(f["payment_gbp"]), btxt))
    s.append("\n## 4. Deliverable Answers\n")
    s.append("### goodwill_fund_return_h1_2026.csv\n")
    s.append("1. One row per month (refunds made; refunds made late; late share in per cent; met the 95 per cent "
             "commitment; goodwill vouchers issued in pounds):")
    for k in months:
        r = m[k]
        s.append("   - %s: %s; %s; %.1f; %s; %s" % (k, c(r["refunds_made"]), c(r["refunds_late"]), r["late_share_pct"],
                                                  r["met"], c(r["vouchers_gbp"])))
    s.append("\n### refund_timeliness_note.pdf\n")
    s.append("1. Payment into the goodwill fund: GBP %s." % c(f["payment_gbp"]))
    s.append("2. Months that broke the commitment: %s 2026." % btxt)
    s.append("3. A bar chart of each month's late share against a dashed 5 per cent commitment line, the breach "
             "months' bars in red and marked missed, on page 1.")
    s.append("4. Vouchers issued in January to June for a refund delay, by the category of the order the refund was on "
             "(vouchers; value in pounds):")
    for k in CATS:
        s.append("   - %s: %s; %s" % (k, c(f["categories"][k]["count"]), c(f["categories"][k]["value_gbp"])))
    open(out_path, "w", encoding="utf-8").write("\n".join(s) + "\n")
