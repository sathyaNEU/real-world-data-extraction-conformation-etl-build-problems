"""submission.md from generator/figures.json: the five blocks, every figure emitted from the generator's own numbers."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402

PP = {"first_purchase_d14", "retained_m6"}
SHORT = {"active_days_d1_14": "active days", "sessions_d1_14": "sessions", "first_purchase_d14": "first purchase",
         "items_saved_d1_14": "items saved", "push_opens_d1_14": "push opens", "retained_m6": "six-month retention"}


def u(m, v):
    return ("%.2f pp" % v) if m in PP else ("%.3f" % v)


def c2(v):
    return "%.2f" % v


def text(fig):
    c, cr, rho = fig["call"], fig["correlations"], fig["components"]["user_level_correlation"]
    B, C, P = fig["asks"]["B"], fig["asks"]["C"], fig["parameters"]
    order = c["order"]
    out = ["## Tags", "",
           "**Domain:** Product Analytics (metric definition and measurement science).",
           "**Analytical objective:** Descriptive & Distribution Analysis.", "",
           "## 1. Final Recommendation", "",
           "**Kleerwissel should adopt first purchase within 14 days (first_purchase_d14) as its 2027 proxy for "
           "six-month retention.**",
           "Across the %d past onboarding changes its effects correlate with the same changes' effects on retained_m6 "
           "at %s, against %s for sessions in days 1 to 14, the runner-up. Not sessions (%s) or active days (%s), "
           "whose measured effects move with retention's largely through the sampling error the two effects share "
           "on the same users. Not items saved (%s) or push opens (%s)." %
           (c["changes"], c2(cr["first_purchase_d14"]), c2(cr["sessions_d1_14"]), c2(cr["sessions_d1_14"]),
            c2(cr["active_days_d1_14"]), c2(cr["items_saved_d1_14"]), c2(cr["push_opens_d1_14"])), "",
           "## 2. Critical Components", "",
           "1. The correlations rest on **%d** changes from **%d** onboarding experiments." % (c["changes"],
                                                                                               c["experiments"]),
           "2. Each candidate's correlation under the standard: first purchase **%s**, sessions **%s**, items saved "
           "**%s**, push opens **%s**, active days **%s**." % tuple(c2(cr[m]) for m in
                                                                    ["first_purchase_d14", "sessions_d1_14",
                                                                     "items_saved_d1_14", "push_opens_d1_14",
                                                                     "active_days_d1_14"]), "",
           "## 3. Step-by-Step Solution", "",
           "1. Took from onboarding_experiments_2024_2026.csv the experiments started from 2024 whose six-month read "
           "closed by 23 October 2026, completed or stopped early, that passed the sample-ratio check (standard section 2): "
           "%d experiments and %d changes, each treatment arm against its control." % (c["experiments"], c["changes"]),
           "2. Read experiment_scorecards_2024_2026.csv at each arm and metric's latest computation, the former keys "
           "through metric_catalogue.yaml, and took each change's effect on each candidate and on retained_m6 "
           "(treatment mean less control mean), the experiment's measurement of the effect the standard correlates, and "
           "its sampling "
           "variance (each arm's variance over its users, summed).",
           "3. Took each candidate's user-level correlation with retained_m6 among the %s users of "
           "global_holdout_users_2025.csv (active days %s, sessions %s, first purchase %s, items saved %s, push opens "
           "%s) and set each change's sampling covariance between its two effects at that correlation times each "
           "arm's two standard deviations over its users, summed over the arms." %
           ("{:,}".format(fig["components"]["holdout_users"]), c2(rho["active_days_d1_14"]),
            c2(rho["sessions_d1_14"]), c2(rho["first_purchase_d14"]), c2(rho["items_saved_d1_14"]),
            c2(rho["push_opens_d1_14"])),
           "4. Correlated each candidate's effects with retention's across the %d changes, each counted once, with the "
           "mean sampling covariance taken out of their covariance and the mean sampling variances out of their "
           "variances: first purchase %s, sessions %s, items saved %s, push opens %s, active days %s." %
           ((c["changes"],) + tuple(c2(cr[m]) for m in ["first_purchase_d14", "sessions_d1_14", "items_saved_d1_14",
                                                        "push_opens_d1_14", "active_days_d1_14"])),
           "5. Calendar: took each ISO week's figure in new_user_forecast_2027.csv once (the tool writes a week's "
           "forecast on each of its days, as the guide's A2 holdout of about 430 a week confirms), set %s per cent "
           "aside for the 2027 holdout, split each layer's users on a "
           "platform evenly among its experiments live that week on that platform and each experiment's users evenly "
           "among its arms (experimentation_platform_guide.pdf A2 to A4), and took %s times each candidate's holdout "
           "standard deviation times the square root of two over the users per arm." %
           (P["holdout_2027_per_cent"], P["z_sum"]),
           "6. Holdout read: took the rows of signup_cohorts_2025.csv for accounts that signed up as consumers, those "
           "now business included, at their latest refresh, took the holdout's own users and sums out of each half's "
           "totals (the table counts every new consumer), and set each half's mean outside the holdout against the "
           "holdout's mean.",
           "7. Named first purchase within 14 days, the highest correlation (%s against sessions' %s)." %
           (c2(cr["first_purchase_d14"]), c2(cr["sessions_d1_14"])), "",
           "## 4. Deliverable Answers", "", "### %s" % K.BOOK, "",
           "1. Proxy for 2027: first purchase within 14 days (first_purchase_d14).",
           "2. Correlation with six-month retention under the standard:"]
    for m in order:
        out.append("   - %s: %s" % (K.LABEL[m][0].upper() + K.LABEL[m][1:], c2(cr[m])))
    out.append("3. Past changes the correlations rest on: %d (%d experiments)." % (c["changes"], c["experiments"]))
    out.append("4. First-quarter 2027 calendar, users per arm and the smallest effect a treatment arm can detect "
               "against its control:")
    for e in sorted(B["users_per_arm"]):
        d = B["detectable"][e]
        out.append("   - %s: %s users per arm; %s" % (e, "{:,}".format(B["users_per_arm"][e]),
                                                      ", ".join("%s %s" % (SHORT[m], u(m, d[m])) for m in K.CAND)))
    out.append("5. 2025 new consumer users outside the global holdout less the holdout's users:")
    for half, name in (("H1", "January to June"), ("H2", "July to December")):
        out.append("   - %s: %s" % (name, ", ".join("%s %s" % (SHORT[m], u(m, C[half][m]))
                                                    for m in K.CAND + [K.RET])))
    out += ["", "### %s" % K.DECK, "",
            "1. Slide 1 names first purchase within 14 days as the 2027 proxy, %s against sessions' %s." %
            (c2(cr["first_purchase_d14"]), c2(cr["sessions_d1_14"])),
            "2. Slide 2: bar chart of each candidate's correlation under the standard, first purchase highlighted.",
            "3. Slides 4 and 5: the calendar's users per arm and detectable effects, and the 2025 holdout read, as in "
            "the workbook.", ""]
    return "\n".join(out)


if __name__ == "__main__":
    task = os.path.dirname(HERE)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    with open(os.path.join(task, "submission.md"), "w", encoding="utf-8") as f:
        f.write(text(fig))
    print("submission.md written")
