"""submission.md for task171, emitted from figures.json."""
import calendar
import os

import common as C


def write(fig):
    n = lambda x: "{:,}".format(x)
    m = lambda x: "$%.2f million" % (x / 1e6)
    L = ["## Tags", "", "**Domain:** Economics & Econometrics (forecasting and forecast evaluation).",
         "**Analytical objective:** Forecasting & Predictive Modeling.", ""]
    L += ["## 1. Final Recommendation", "",
          "**Put %s in the 2027 revenue certificate as the toll collected on the toll billed by mail to today's cash-lane users.** "
          "An in-state invoice unpaid at 60 days is collected when its plate next renews its two-year registration, so the "
          "in-state share is read on the held invoices whose registration on file has since expired: %d per cent in-state and "
          "%d per cent out-of-state. Not the share of invoices a year old, which counts in-state invoices still waiting on a "
          "renewal. Not the share across every toll-by-mail and violation invoice, which mixes in the violators."
          % (m(fig["call_collected_toll_2027_usd"]), fig["call_share_in_state_pct"], fig["call_share_out_of_state_pct"]), ""]
    L += ["## 2. Critical Components", "",
          "1. Share of in-state toll billed by mail eventually collected: **%d per cent**." % fig["call_share_in_state_pct"],
          "2. Share of out-of-state toll billed by mail eventually collected: **%d per cent**." % fig["call_share_out_of_state_pct"], ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Took the overnight toll-by-mail invoices (invoice_type TOLL-BY-MAIL in %s) and applied each invoice's payments in %s "
          "posted to 31 October 2026, net of reversals, toll first." % (C.F_INV, C.F_PAY),
          "2. In-state, among invoices at least 61 days old, %.1f per cent of the toll was paid within 60 days of issue." % fig["early_share_in_state_pct"],
          "3. For the in-state toll still unpaid at 60 days, joined %s: of the held invoices whose registration on file (reg_expires) "
          "had expired by 31 October 2026, %.1f per cent of the toll was paid; invoices with no Division record were read on "
          "those a year old, as the agency had closed them." % (C.F_MVD, fig["renewal_share_in_state_pct"]),
          "4. Combined the two: %d per cent of in-state toll is eventually collected; out-of-state, the invoices issued a year or "
          "more before 31 October 2026 collected %d per cent." % (fig["call_share_in_state_pct"], fig["call_share_out_of_state_pct"]),
          "5. Applied the shares to the 2027 toll billed by mail in %s ($%s in-state, $%s out-of-state): %s, to the nearest $0.25 million."
          % (C.F_PLAN, n(C.PLAN_TOLL["IS"]), n(C.PLAN_TOLL["OS"]), m(fig["call_collected_toll_2027_usd"])),
          "6. For the violation tables, counted each express-lane vehicle read in both lanes within a second once, and dropped "
          "violation lines read 0.4 seconds or less behind a commercial posting in the same lane in %s (a trailer or towed car "
          "split off a MarrowPass truck), then counted crossings and summed toll by month of crossing." % C.F_TAG,
          "7. For the out-of-state violation invoices, applied each agency settlement in %s (no invoice number; its reference "
          "lists the invoices) oldest invoice first, toll before fees, and divided the toll collected on owed crossings by the "
          "toll owed, by quarter of issue." % C.F_PAY, ""]
    L += ["## 4. Deliverable Answers", "", "### aet_2027_toll_by_mail_forecast.xlsx", "",
          "1. Toll collected in 2027 on the toll billed by mail to today's cash-lane users: %s." % m(fig["call_collected_toll_2027_usd"]),
          "2. Share eventually collected: in-state %d per cent; out-of-state %d per cent." % (fig["call_share_in_state_pct"], fig["call_share_out_of_state_pct"]),
          "3. Violation crossings and toll owed, by month of crossing in 2026:"]
    for mo in range(1, 10):
        L.append("   - %s: %s crossings, $%s owed" % (calendar.month_name[mo], n(fig["a_2026_%02d_crossings" % mo]), "{:,.2f}".format(fig["a_2026_%02d_toll_owed_usd" % mo])))
    L.append("4. Out-of-state violation invoices, share of toll owed collected by 31 October 2026, by quarter of issue:")
    for q, lab in [("2025q2", "April to June 2025"), ("2025q3", "July to September 2025"), ("2025q4", "October to December 2025"), ("2026q1", "January to March 2026")]:
        L.append("   - %s: %d per cent" % (lab, fig["b_%s_collected_pct" % q]))
    open(os.path.join(C.TASK, "submission.md"), "w").write("\n".join(L) + "\n")
