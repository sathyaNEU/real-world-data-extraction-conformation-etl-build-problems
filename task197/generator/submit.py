"""task197 submission.md, written from generator/figures.json so every figure is emitted, never typed."""
import os, sys, json, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world

TASK = os.path.dirname(HERE)
F = json.load(open(os.path.join(HERE, "figures.json")))
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
HALF = {"2025 H1": "January to June 2025", "2025 H2": "July to December 2025", "2026 H1": "January to June 2026"}
WORDS = {6: "six", 8: "eight"}


def month(ym):
    y, m = ym.split("-")
    return "%s %s" % (MONTHS[int(m) - 1], y)


def day(iso):
    d = dt.date.fromisoformat(iso)
    return "%d %s %d" % (d.day, MONTHS[d.month - 1], d.year)


def e1(x):
    return "%.1f" % x


def main():
    eff = {e["code"]: e for e in F["effects"]}
    call, run = eff[F["call_code"]], eff[F["runner_up_code"]]
    others = [e for e in F["effects"] if e["code"] not in (F["call_code"], F["runner_up_code"])]
    n = WORDS[len(F["effects"])]
    thr = "%.2f" % F["threshold"]
    short = call["product"].split(" Acetaminophen")[0]
    nic_short = run["product"].split(" Nicotine")[0]
    L = []
    L += ["## Tags", "",
          "**Domain:** Pharmacology, Pharmacoepidemiology & Safety (safety signal detection).",
          "**Analytical objective:** Anomaly Detection & Diagnostics.", ""]
    L += ["## 1. Final Recommendation", "",
          "**We should refer %s to the 2027 Child-Resistant Packaging Review: its packaging change had an effect of "
          "%s, the only one of the %s changes to reach %s.** The runner-up is %s at %s, a gap of %s. Not Dozinox "
          "Nighttime Sleep-Aid, which leads on exposures per pack sold only because it sold far fewer packs after its "
          "move to blisters while the bottles bought before stayed in homes; not %s on its raw rise, which its tripled "
          "pack sales carried." % (call["product"], e1(call["effect"]), n, thr, run["product"], e1(run["effect"]),
                                   e1(F["gap"]), nic_short), ""]
    L += ["## 2. Critical Components", "",
          "1. %s's changed pack was first sold at retail on %s, so its twelve months run %s to %s, with **%s** "
          "accidental exposures of children under six recorded." % (short, day(call["change"]), month(call["window"][0]),
                                                                   month(call["window"][1]), "{:,}".format(call["observed"])),
          "2. Against the exposures its packs in use would have produced with the previous cap, its effect is **%s**, "
          "the only effect of at least **%s**." % (e1(call["effect"]), thr),
          "3. %s recorded **%s** from %s to %s, an effect of **%s**; the gap between the two effects is **%s**." % (
              run["product"], "{:,}".format(run["observed"]), month(run["window"][0]), month(run["window"][1]),
              e1(run["effect"]), e1(F["gap"])), ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Took the %s packaging changes first sold at retail between 1 January 2024 and 30 September 2025 from the "
          "Packaging changes sheet of watched_products_register.xlsx, each with its date of first retail sale "
          "(procedure CRP-3, sections 2 and 3.3)." % n,
          "2. Counted the lines of case_export_watched_products.csv with reason Unintentional - general, "
          "patient_age_years under six and the product's product_code, by calendar month of call_received_local "
          "(sections 3.2 and 3.3): %s has %s in its twelve months." % (short, "{:,}".format(call["observed"])),
          "3. Rebuilt each product's daily packs sold from halcyon_pos_4wk_revised.csv, taking "
          "halcyon_pos_4wk_preliminary.csv only for the period the revision lacks, spreading each four-week period's "
          "units evenly over its days and summing the product's UPCs and channels.",
          "4. Modelled each product's monthly exposures as a constant rate times its packs in use, every day's "
          "purchases draining geometrically at the product's own pace, and fitted the rate and the pace by Poisson "
          "likelihood to the product's months from January 2019 to the month before its change month.",
          "5. Back-tested the model on each product's last year before its change, fitted on the years before: it "
          "predicts every held-out year far better than a constant rate per pack sold, and %s's better than a time "
          "series on sales and trend." % short,
          "6. Ran each fitted model through the product's twelve months for the exposures expected with the previous "
          "packaging and divided the recorded count by it: %s %s, %s %s, the other %s %s." % (
              short, e1(call["effect"]), nic_short, e1(run["effect"]), WORDS[len(others)], e1(others[0]["effect"])),
          "7. For the asks, read antidote_preparations_2024-07_2026-10.csv by hospital: an acetylcysteine course is a "
          "first bag with the later bags whose doses fit the three-bag or the two-bag regimen at the weight that first "
          "bag implies and at the regimen's hours, and a deferoxamine course for an iron poisoning is a chain of "
          "same-dose bags about eight hours apart, leaving out the bags of one dose prepared on consecutive evenings "
          "for transfusion admissions; courses are counted in the half-year their first bag was prepared.",
          "8. Applied section 4: %s has the largest effect and the only one of at least %s, so it is referred, with "
          "%s the runner-up and a gap of %s." % (short, thr, nic_short, e1(F["gap"])), ""]
    L += ["## 4. Deliverable Answers", "", "### packaging_referral.docx", "",
          "1. Product referred: %s (%s)" % (call["product"], call["product_code"]),
          "2. Its effect: %s" % e1(call["effect"]),
          "3. Runner-up: %s (%s), effect %s" % (run["product"], run["product_code"], e1(run["effect"])),
          "4. Gap between their effects: %s" % e1(F["gap"]), "",
          "### referral_tables.xlsx", "",
          "1. Every watched product whose packaging changed, its effect and whether it reaches %s:" % thr]
    for e in F["effects"]:
        L.append("   - %s: %s, %s" % (e["product"], e1(e["effect"]),
                                       "reaches %s" % thr if e["reaches"] else "does not reach %s" % thr))
    L.append("2. Courses started, each hospital and half-year (acetylcysteine; deferoxamine for an iron poisoning; "
             "the two together), whole numbers:")
    for a in F["antidote"]:
        L.append("   - %s, %s: %d; %d; %d" % (a["name"], HALF[a["half"]], a["acetylcysteine_courses"],
                                               a["deferoxamine_courses"], a["antidote_courses"]))
    L += ["", "### effects_chart.png", "",
          "1. One dot per changed product at its effect, labelled to one decimal, against a dashed referral line at "
          "%s; %s is highlighted as the only product past the line." % (thr, short), ""]
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(L))
    print("submission.md written")


if __name__ == "__main__":
    main()
