"""Write task155/submission.md from generator/figures.json (every number emitted, none typed)."""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
STORES = ["Altona", "Ballarat", "Box Hill", "Camberwell", "Ringwood", "Sunshine", "Werribee", "Williamstown"]


def n(x):
    return "{:,}".format(x)


def h1(x):
    return "{:,.1f}".format(x)


def key(s):
    return s.lower().replace(" ", "_")


def text(F):
    w = []
    a = w.append
    a("## Tags")
    a("")
    a("**Domain:** Economics & Econometrics (discrete-choice and limited-dependent-variable modelling: casual staff's "
      "take-up of extra shifts offered through call-in).")
    a("**Analytical objective:** Forecasting & Predictive Modeling.")
    a("")
    a("## 1. Final Recommendation")
    a("")
    a("**Place the relief crew at %s; it will work %s hours there.**" % (F["call_store"], n(F["crew_hours"])))
    a("Call-ins would leave more of %s's open Christmas hours unfilled than of any other store's, because its uplift "
      "runs 10 am to 4 pm on weekdays, when most of its casuals are unavailable, and almost none of it carries on from "
      "a casual's rostered shift. Not Werribee, which lists the "
      "most open hours (%s) but whose open shifts carry on from its own casuals' rostered shifts, the offer casuals take "
      "%d%% of the time against %d%% for a separate trip in; not Box Hill or Altona, whose evening uplift sits behind "
      "their casuals' afternoon shifts in the same way."
      % (F["call_store"], n(F["open_hours_werribee"]), F["ext_rate_pct"], F["other_rate_pct"]))
    a("")
    a("## 2. Critical Components")
    a("")
    a("1. Offers that start as the casual's own rostered or booked shift at that store ends, or end as it starts, are "
      "accepted **%d%%** of the time, against **%d%%** for every other offer." % (F["ext_rate_pct"], F["other_rate_pct"]))
    a("2. **%d%%** of Werribee's open Christmas shifts could be taken by one of its own casuals staying on from a "
      "rostered shift that ends as the open shift starts or starts as it ends, the module's checks passed (Box Hill "
      "**%d%%**, Altona **%d%%**), against **%d%%** of Camberwell's."
      % (F["abut_pct_werribee"], F["abut_pct_box_hill"], F["abut_pct_altona"], F["abut_pct_camberwell"]))
    a("3. Camberwell's %d open shifts carry **%s** paid hours to the nearest 10." % (F["open_shifts_camberwell"],
                                                                                n(F["crew_hours"])))
    a("")
    a("## 3. Step-by-Step Solution")
    a("")
    a("1. Summed the paid hours (less the unpaid meal break on shifts over five hours, per "
      "ea_2024_casual_employment_summary.pdf) of the OPEN lines on each sheet of christmas_roster_2026_published.xlsx: "
      "Werribee %s hours, Box Hill %s, Altona %s, Camberwell %s."
      % (n(F["open_hours_werribee"]), n(F["open_hours_box_hill"]), n(F["open_hours_altona"]),
         n(F["open_hours_camberwell"])))
    a("2. Joined every offer in callin_offers_20250829_20261112.csv to the casual's roster lines that day (person code "
      "to payroll number through kws_people_20261112.csv and the previous numbers in "
      "payroll_casual_register_20261112.csv; both roster exports, less lines callin_register_20250829_20261112.csv "
      "shows vacated, plus call-ins the casual had accepted): %s offers carried on from the casual's own shift at the "
      "store and %d%% of them were accepted, against %d%% of the other %s."
      % (n(F["ext_offers"]), F["ext_rate_pct"], F["other_rate_pct"], n(F["other_offers"])))
    a("3. Fitted a logit of each offer's acceptance on that term and on another shift the same day, a Sunday shift, the "
      "shift's paid hours, finishing after 21:30, starting before 07:00, under four hours' notice, an offer repeated, a "
      "sister-store offer, rostered hours over 10 that week, the Christmas weeks, the casual's age band and home store.")
    a("4. Ran the fitted choice through the offer order, eligibility checks and offer hours in "
      "kws_callin_module_notes.pdf over the published Christmas rosters, every store's open shifts posted at 09:00 on "
      "Monday 16 November with the crew at no store (relief_crew_placement_standard.pdf, section 4), %d runs: "
      "call-ins would leave about %s of Camberwell's open hours unworked, the most of any store, with %s next at "
      "about %s." % (F["runs"], n(F["unworked_camberwell"]), F["runner_up"],
                     n(F["unworked_" + F["runner_up"].lower().replace(" ", "_")])))
    a("5. Placed the crew at %s under section 3 of the standard; its crew hours under section 5 are the paid hours of "
      "%s's open shifts: %s." % (F["call_store"], F["call_store"], n(F["crew_hours"])))
    a("")
    a("## 4. Deliverable Answers")
    a("")
    a("### relief_crew_placement_xmas2026.pdf")
    a("")
    a("1. The placement in the opening sentence: the relief crew to %s, %s crew hours." % (F["call_store"],
                                                                                        n(F["crew_hours"])))
    a("2. A horizontal bar chart of every store's forecast unworked hours, largest first, %s highlighted, each bar "
      "labelled, titled with the finding." % F["call_store"])
    a("")
    a("### relief_crew_xmas2026.xlsx")
    a("")
    a("1. Last Christmas's call-ins, 28 November to 24 December 2025, paid hours: put out to call-in, covered, left "
      "uncovered:")
    for s in STORES:
        k = key(s)
        a("   - %s: %s, %s, %s" % (s, h1(F["A_put_out_%s" % k]), h1(F["A_covered_%s" % k]), h1(F["A_uncovered_%s" % k])))
    a("2. Cover across stores in those weeks, paid hours: the store's call-ins covered by casuals from other stores; "
      "its own casuals' cover at other stores:")
    for s in STORES:
        k = key(s)
        a("   - %s: %s; %s" % (s, h1(F["B_imports_%s" % k]), h1(F["B_exports_%s" % k])))
    return "\n".join(w) + "\n"


def write(task):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    with open(os.path.join(task, "submission.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text(F))


if __name__ == "__main__":
    write(os.path.dirname(HERE))
