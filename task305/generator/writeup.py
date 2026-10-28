"""submission.md from figures.json."""
import solve as S


def f0(x):
    return format(int(round(x)), ",")


def write(path, fig):
    c, b, r, ask, rt = fig["call"], fig["by_app"], fig["response"], fig["ask"], fig["routes"]
    win, run = c["app"], c["runner_up"]
    l0 = rt["L0 the heavy accounts' own upgrades, nobody leaving"]
    l2 = rt["L2 the stopped accounts' upgrade share, nobody leaving"]
    l3 = rt["L3 every account that does not upgrade leaves"]
    lo = min(v[win] for v in fig["standing"].values())
    hi = max(v[win] for v in fig["standing"].values())
    pc = fig["shares_pct"]
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** Product Analytics, churn propensity and uplift modelling (a software company's choice of which "
               "of five apps takes a three-project limit on its free plan first, sized by the 2027 revenue the limit adds, "
               "with free accounts' response read from the accounts the free plan's storage allowance already stops, "
               "and each app's recurring revenue bridge from its billing records).")
    out.append("**Analytical objective:** Opportunity Sizing & Decision Support.\n")
    out.append("## 1. Final Recommendation\n")
    out.append("**Brindlecote should take the three-project limit first in %s, where it adds about GBP %s to 2027 revenue.**"
               % (win, f0(c["addition_rounded"])))
    out.append("The limit adds GBP %s to %s's 2027 revenue as built (GBP %s to %s across the standing variants of its "
               "construction), against GBP %s in %s, the next best. The free plan already stops accounts at its two-gigabyte "
               "storage allowance: the month after an account reaches it, %.1f per cent are on Plus and %.1f per cent have "
               "stopped using the app, and over the following year a stopped account spends %.2f more months on Plus and %.1f fewer "
               "months on the free plan than an unstopped account over three projects. %s's GBP %.2f Plus price outweighs "
               "the free-plan revenue (GBP %.2f a month) each leaver takes with it. Not Tracewood, which the free accounts' "
               "own upgrade rate with nobody leaving puts first (GBP %s against GBP %s for %s): an account the limit stops "
               "is not an account upgrading of its own accord, and the leavers cost Tracewood GBP 2.00 a month each. Not "
               "%s either, which counting every account that does not pay as lost puts first."
               % (f0(c["addition"]), win, f0(lo), f0(hi), f0(c["runner_up_addition"]), run, pc["plus_next_month"],
                  pc["gone_next_month"], r["plus_months_gained"], r["free_months_lost"], win, b[win]["plus_price"],
                  b[win]["free_revenue"], f0(l0["Tracewood"]), f0(l0[win]), win,
                  max(l3, key=lambda a: l3[a])))
    out.append("\n## 2. Critical Components\n")
    out.append("1. The month after a free account first reached the storage allowance (January 2023 to September 2025, "
               "%s accounts in the research panel), **%.1f per cent** were on Plus and **%.1f per cent** had stopped "
               "using the app, alike across apps, project counts and account ages, while free accounts over three projects "
               "move to Plus on their own at about **%.1f per cent a year**." % (f0(r["stops"]), pc["plus_next_month"],
                                                                                  pc["gone_next_month"], pc["own_plus_12"]))
    out.append("2. Set against unstopped free accounts over three projects, a stopped account gains **%.2f months on Plus** "
               "and loses **%.1f months of free use** in the year after the stop." % (r["plus_months_gained"],
                                                                                      r["free_months_lost"]))
    out.append("3. The limit reaches **%s** free accounts over three active projects in %s and **%s** more reaching a "
               "fourth during 2027, and adds **GBP %s** to %s's 2027 revenue (about GBP %s), more than in any other app "
               "(%s GBP %s)." % (f0(b[win]["over_three"]), win, f0(b[win]["reaching_four_2027"]), f0(c["addition"]), win,
                                 f0(c["addition_rounded"]), run, f0(c["runner_up_addition"])))
    out.append("\n## 3. Step-by-Step Solution\n")
    steps = [
        "Read free_plan_limit_paper_2027.pdf: the limit stops a free account over three active projects from editing until "
        "it archives or moves to Plus; the addition is the app's 2027 revenue with the limit less without it, a month on Plus "
        "at the Plus price and a month of free use at the free-plan revenue per active free account (section 4), the limit "
        "reaching every free account over three active projects on 1 January 2027 and every one reaching a fourth during the year.",
        "Built each research panel account's months from research_panel_account_months_2023_2026.csv (Leafnote read as "
        "Notewell before April 2025): plan, active projects, storage and whether it was used that month; an account with no "
        "row in a month was not used.",
        "Found the free plan's existing stop in plan_catalogue_2026.csv (2 GB, 2,048 MiB, of storage on the free plan) and the "
        "free account-months at it (storage within one per cent of 2,048 MiB): %s accounts reached it for the first time from "
        "January 2023 to September 2025, each followed for twelve months." % f0(r["stops"]),
        "Compared them with free accounts over three active projects below the allowance in the same months (the accounts the "
        "limit stops, as they act unstopped), month by month for a year: %.2f more months on Plus and %.1f fewer months of free "
        "use for a stopped account." % (r["plus_months_gained"], r["free_months_lost"]),
        "Took the accounts the limit reaches from free_accounts_by_active_projects_2023_2026.xlsx for %s (bands 4-5, 6-9 and 10+), "
        "and the accounts reaching a fourth active project each month of a year from the panel's accounts below four in "
        "September 2025, applied to each app's accounts with three or fewer." % fig["kpi_month"],
        "Valued each app's year: the accounts over the limit on 1 January for twelve months after the stop and each month's new "
        "arrivals for the rest of the year, at the paper's Plus price and free-plan revenue: %s." % "; ".join(
            "%s GBP %s" % (a, f0(b[a]["addition"])) for a in S.APPS),
        "Checked the standing variants (every stop rather than the first, the allowance read at 2,000, 1,950 or 2,047 MiB, "
        "every unstopped free account as the comparison, the stops of one year, a year's crossings to September 2024, each "
        "app read from its own stopped accounts, only accounts with four or more projects): %s stays first, GBP %s to %s." % (
            win, f0(lo), f0(hi)),
        "For the bridge, valued every subscription on FIN-07 (recurring_revenue_policy_fin07.pdf): a monthly price as it is, "
        "an annual price over twelve, seat price times seats, after discounts of twelve months or more, euros and dollars at "
        "the 2026/27 plan rates in fx_plan_rates.csv; live from billing_subscriptions_20250930.csv and the events to the end "
        "of 30 September 2026 (a cancellation ends a subscription at its subscription.ended event, a past-due subscription "
        "stays live).",
        "Took the customer as the person or organisation that pays: a subscription opened under a new customer record by the "
        "same account the day the platform ended its old one after failed payments is the same customer, and staff accounts' "
        "Plus subscriptions a company record moved onto one Team subscription stay with that company; then compared each "
        "customer's recurring revenue at the two dates, app by app.",
    ]
    for i, s in enumerate(steps, 1):
        out.append("%d. %s" % (i, s))
    out.append("\n## 4. Deliverable Answers\n")
    out.append("### free_plan_limit_2027.xlsx\n")
    out.append("1. App to take the three-project limit first: %s." % win)
    out.append("2. What it adds to %s's 2027 revenue: GBP %s (nearest GBP %s; GBP %s as built)." % (
        win, f0(c["addition_rounded"]), f0(fig["rounding_gbp"]), f0(c["addition"])))
    out.append("3. Each app's 2027 addition behind the call: %s." % "; ".join("%s GBP %s" % (a, f0(b[a]["addition"]))
                                                                         for a in S.APPS))
    out.append("4. Each app's recurring revenue movements from 30 September 2025 to 30 September 2026, GBP a month (new, "
               "expansion, contraction, churned):")
    for a in S.APPS:
        out.append("   - %s: new %s, expansion %s, contraction %s, churned %s" % (
            a, f0(ask["%s new" % a]), f0(ask["%s expansion" % a]), f0(ask["%s contraction" % a]), f0(ask["%s churned" % a])))
    out.append("\n### free_plan_limit_case_2027.docx\n")
    out.append("1. The case for the executive: take the limit first in %s, about GBP %s added to its 2027 revenue, read "
               "from the accounts the storage allowance already stops; not Tracewood, which only the free accounts' own "
               "upgrades with nobody leaving put first." % (win, f0(c["addition_rounded"])))
    with open(path, "w") as fh:
        fh.write("\n".join(out) + "\n")
