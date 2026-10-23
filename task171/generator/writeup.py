"""submission.md for task171, emitted from figures.json."""
import json
import os

import common as C


def write(fig):
    n = lambda x: "{:,}".format(x)
    L = []
    L += ["## Tags", "", "**Domain:** Economics & Econometrics (discrete choice and limited dependent variable modeling).",
          "**Analytical objective:** Forecasting & Predictive Modeling.", ""]
    L += ["## 1. Final Recommendation", "",
          "**Budget for %s R-1 services moved to R-ON by December 31, 2027, giving up $%s a year at test-year use.** "
          "Members take an optional rate by what it saves them on their own use, so the overnight rate's take-up is the evening "
          "rate's first-year response to each service's saving on its use in the year before that offer, run through each "
          "service's overnight saving. Not the evening rate's take-up applied at the average member's bill change, which "
          "ignores who takes an optional rate. Not the same response read on the latest year's use, which the evening rate's "
          "takers had already changed by taking it." % (n(fig["call_members_2027"]), n(fig["call_shortfall_2027_usd"])), ""]
    L += ["## 2. Critical Components", "",
          "1. The forecast population is **%s** R-1 services billed in all twelve test-year months." % n(fig["population_2026"]),
          "2. Of the **%s** R-1 services open when R-TOU opened in March 2024, **%s** had it in effect by the February 2025 read." % (n(fig["cohort_2024"]), n(fig["takers_first_year_2024"])),
          "3. The services moved to R-ON by December 31, 2027 are **%s**, giving up **$%s** a year." % (n(fig["call_members_2027"]), n(fig["call_shortfall_2027_usd"])), ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Took from %s and %s the R-1 services open when R-TOU opened in March 2024 (%s) and the month each first had R-TOU in effect, "
          "%s by the February 2025 read, a service leaving the risk set at its final read." % (C.F_RATE, C.F_SVC, n(fig["cohort_2024"]), n(fig["takers_first_year_2024"])),
          "2. Priced each of those services' R-1 and R-TOU bills at the 2024 prices in %s on its own use in billing months "
          "March 2023 to February 2024 in %s, and fitted a monthly logit hazard of R-TOU taking effect on that saving with a "
          "term for each month since the offer." % (C.F_SCHED, C.F_AMI),
          "3. Took the population of paper RC-26-19 in %s, %s R-1 services at October 31, 2026 billed in all twelve billing "
          "months November 2025 to October 2026, and priced each one's R-1 and R-ON bills on the 2027 schedules on that use." % (C.F_PLAN, n(fig["population_2026"])),
          "4. Ran each population service's saving through the fitted hazard over the twelve months of 2027 and summed the "
          "probabilities and the probability-weighted savings: %s services and $%s." % (n(fig["call_members_2027"]), n(fig["call_shortfall_2027_usd"])),
          "5. For the R-TOU table, joined each service's contiguous R-TOU rows into one spell (the TOU module re-writes the row "
          "at account maintenance), ended an open R-TOU row at the service's final read, kept the re-collected actual row "
          "where the extract holds an estimate and an actual for one meter and read period, and summed the kWh by district.",
          "6. For the requests table, converted received_utc in %s to Central time, dropped cases closed as duplicates, placed "
          "each completed case in the district of the service that had R-TOU take effect at the next read after the case was "
          "completed (the case's service or the same member's other service) and each other case at the service it names." % C.F_CRM,
          "7. Filed %s services and $%s for the 2027 budget." % (n(fig["call_members_2027"]), n(fig["call_shortfall_2027_usd"])), ""]
    L += ["## 4. Deliverable Answers", "", "### r-on_2027_forecast.xlsx", "",
          "1. R-1 services moved to R-ON by December 31, 2027: %s." % n(fig["call_members_2027"]),
          "2. Annual revenue those services give up at test-year use: $%s." % n(fig["call_shortfall_2027_usd"]),
          "3. Services on R-TOU at October 31, 2026, by district:"]
    for d in C.DISTRICTS:
        k = C.DCODE[d]
        L.append("   - %s: %s on it without a break since November 1, 2025 or earlier; %s kWh 4 p.m. to 9 p.m.; %s kWh 11 p.m. to 6 a.m."
                 % (d, n(fig["a_%s_twelve_months" % k]), n(fig["a_%s_kwh_4to9pm" % k]), n(fig["a_%s_kwh_11pmto6am" % k])))
    L.append("4. R-TOU enrolment requests received March 1 to May 31, 2024, by district:")
    for d in C.DISTRICTS:
        k = C.DCODE[d]
        L.append("   - %s: %s requests, %s through the web form" % (d, n(fig["b_%s_requests" % k]), n(fig["b_%s_web" % k])))
    open(os.path.join(C.TASK, "submission.md"), "w").write("\n".join(L) + "\n")
