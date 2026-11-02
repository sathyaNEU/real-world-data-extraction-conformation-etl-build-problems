"""task464 architecture 12: submission.md, drafted from figures.json so every figure is emitted, never typed."""
import json
import os

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)


def c(n):
    return "{:,}".format(int(n))


def main(fig=None):
    f = fig or json.load(open(os.path.join(HERE, "figures.json")))
    rs = ["RS-2604", "RS-2605", "RS-2606", "RS-2607", "RS-2608", "RS-2609"]
    dates = [d.strftime("%d %b %Y").lstrip("0") for d in W.SENDS]
    a1, a2 = f["restarted_by_people"], f["clicked_within_28_days"]
    L = []
    L += ["## Tags", "",
          "**Domain:** Product Analytics (churn, propensity and uplift modelling).",
          "**Analytical objective:** Opportunity Sizing & Decision Support.", ""]
    L += ["## 1. Final Recommendation", "",
          "**Drop the restart-your-alerts email from Quaywork's 2027 jobseeker email plan: its thirteen sends would "
          "cost about %s sponsored clicks a year.** The pilot's sends brought back %s clicks among the paused pool "
          "but cost %s among jobseekers with alerts on at Google, Microsoft and Yahoo addresses. Not the holdout "
          "uplift carried forward, which counts only the paused pool and misses the clicks the sends cost everyone "
          "else." % (c(-f["series_2027_clicks"]), c(f["pilot_uplift_clicks"]), c(f["pilot_loss_clicks"])), ""]
    L += ["## 2. Critical Components", "",
          "1. The pilot's gain among the paused pool, mailed arm against the holdout, is **%s** sponsored clicks."
          % c(f["pilot_uplift_clicks"]),
          "2. The pilot's loss among jobseekers with alerts on, at Google, Microsoft and Yahoo addresses, is **%s** "
          "sponsored clicks." % c(f["pilot_loss_clicks"]),
          "3. The pilot's net effect is **%s** sponsored clicks, and the 2027 series at the average send thirteen "
          "times is **%s** a year." % (c(f["pilot_net_clicks"]), c(f["series_2027_clicks"])), ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Counted the 20 to 22 October 2026 reload in sponsored_clicks_by_mailbox_daily.csv once and summed "
          "app_ios and app_android into app.",
          "2. Compared restart_pilot_mailed with restart_pilot_holdout clicks per jobseeker over the six 28-day "
          "windows from 14 April 2026 (%s against %s): the mailed arm gained %s clicks."
          % (f["mailed_clicks_per_jobseeker"], f["holdout_clicks_per_jobseeker"], c(f["pilot_uplift_int"])),
          "3. Read each mailbox group's alerts_on clicks per jobseeker in the 14 days after each send against its own "
          "fortnight before: gmail, microsoft and yahoo_aol fall after every send, the other six groups do not.",
          "4. Measured gmail, microsoft and yahoo_aol on every channel over days 0 to 13 after each send against "
          "the other six groups' pooled rate, at each group's ratio on days 14 to 27 of the window: %s clicks lost."
          % c(f["pilot_loss_int"]),
          "5. Netted the two (%s over the pilot), divided by six sends and multiplied by thirteen: %s clicks a year "
          "in 2027." % (c(f["pilot_net_int"]), c(f["series_2027_int"])),
          "6. Left out each restart whose RS-26xx email had four or more links clicked by the subscriber inside ten "
          "seconds in postvane_clicks_restart_series_2026.csv (a gateway's pass, %s of %s logged restarts)."
          % (c(f["gateway_restarts_removed"]), c(f["restarts_logged_total"])),
          "7. Tied each logged-out app click in restarted_jobseekers_sponsored_clicks.csv to the one account its "
          "app_install_id carries there or in alert_restarts_pilot_pool_2026.csv, then counted restarters with a "
          "sponsored click, before or after restarting, dated in the 28 days starting on their send's date.",
          "8. The series stays only if it adds sponsored clicks (jobseeker_email_plan_2027.docx, section 5); it "
          "costs them, so it is dropped.", ""]
    L += ["## 4. Deliverable Answers", "", "### restart_series_2027.xlsx", "",
          "1. Recommendation: drop the restart series; the 2027 series would cost %s sponsored clicks a year."
          % c(-f["series_2027_clicks"]),
          "2. Gain among the paused pool over the pilot: %s sponsored clicks." % c(f["pilot_uplift_clicks"]),
          "3. Loss among jobseekers with alerts on over the pilot: %s sponsored clicks, at Google, Microsoft and "
          "Yahoo addresses." % c(f["pilot_loss_clicks"]),
          "4. Net effect of the pilot: %s sponsored clicks." % c(f["pilot_net_clicks"]),
          "5. Each pilot send's restarts by people and, of them, those who clicked a sponsored job in the 28 days "
          "starting on the send's date, before or after restarting:"]
    for k in range(6):
        L.append("   - Send %d, %s: %s restarted, %s clicked" % (k + 1, dates[k], c(a1[k]), c(a2[k])))
    L += ["", "### restart_series_2027.docx", "",
          "1. The recommendation to drop the restart series, the 2027 series costing %s sponsored clicks a year."
          % c(-f["series_2027_clicks"]),
          "2. One bar chart of each pilot send's restarts by people beside those who clicked a sponsored job in the 28 "
          "days starting on the send's date.", ""]
    open(os.path.join(BASE, "submission.md"), "w").write("\n".join(L))


if __name__ == "__main__":
    main()
