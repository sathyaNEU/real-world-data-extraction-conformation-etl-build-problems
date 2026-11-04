"""submission.md, drafted from figures.json and nothing else."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
DESK = {"W01": "Fenmoor", "W02": "Callowby", "W03": "Hatherby", "W04": "Tollinghurst", "W05": "Kestrow",
        "W06": "Wellanby"}


WORDS = {0: "none", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}


def c(n):
    return "{:,}".format(n)


def h(x):
    return "{:,.1f}".format(x)


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    ws_order = sorted(DESK, key=lambda w: -F["b_by_ws"][w])
    lines = []
    a = lines.append
    a("## Tags")
    a("")
    a("**Domain:** Human Factors & Ergonomics, safety incident and error analysis (signaller error at a rail "
      "operating centre).")
    a("**Analytical objective:** Root-Cause Analysis.")
    a("")
    a("## 1. Final Recommendation")
    a("")
    a("**Fund programme B, the workstation display renewal: its cause produced %s of the operating centre's delay "
      "minutes in the twelve months to 30 September 2026.** Not signaller competence training (A), which the local "
      "investigations' findings put first, because the wrong routes they book to competence are slips onto an exit "
      "drawn beside the one required, made as often by experienced signallers. Not the seventh workstation (E), whose "
      "case rests on peak-hour error rates that come from those drawn-close routes carrying the peaks' requests. Not "
      "eight-hour shifts (C) or the ARS data rebuild (D), whose incidents carry fewer minutes even counted in full."
      % c(F["call_minutes"]))
    a("")
    a("## 2. Critical Components")
    a("")
    a("1. Wrong routes set onto the exit drawn beside the required one: **%d** incidents, **%s** minutes." % (
        F["slip_count"], c(F["slip_minutes"])))
    a("2. Workstation display faults: **%d** incidents, **%s** minutes." % (F["eq_count"], c(F["eq_minutes"])))
    a("3. The display renewal's minutes are highest on **%s %s**, at **%s**, where its delivery begins." % (
        F["start_ws"], F["start_ws_name"], c(F["b_by_ws"][F["start_ws"]])))
    a("")
    a("## 3. Step-by-Step Solution")
    a("")
    a("1. Kept the incidents in both operating incident registers that occurred from 1 October 2025 to 30 September "
      "2026, UK time, per terms of reference 2.2.")
    a("2. Totalled each incident's primary and reactionary minutes in ocf_delay_records_2025-04_2026-09.csv and "
      "applied the moves attribution_reviews_2025-26_2026-27.csv records as agreed, per terms of reference 2.4.")
    a("3. Mapped each wrong route's route set and route required to their exit signals through the routes in "
      "workstation_layout_export_r8.2.1.json and measured the two exits' buttons on their screen: %d were drawn "
      "%s to %s pixels apart, the other %d wrong routes %s pixels or more." % (
          F["slip_count"], F["gap_close_min_px"], F["gap_close_max_px"], F["rs1_far"], c(int(F["gap_far_min_px"]))))
    a("4. Read roc_signaller_actions_20251001_20260930.csv: of the %d routes cancelled within twenty seconds of being "
      "set, all but %s were followed from the same entrance by a request for the exit drawn beside the one cancelled, "
      "and at the drawn-close routes slips run alike for first-two-years and other signallers and in quiet and busy "
      "hours, so only the renewal's redraw would have prevented the %d, per terms of reference 2.3." % (
          F["quick_cancels"], WORDS[F["quick_cancels"] - F["quick_cancels_beside"]], F["slip_count"]))
    a("5. Added the workstation display faults the renewal's new display system removes: the display renewal's cause "
      "produced %s minutes, more than any other programme's cause." % c(F["call_minutes"]))
    a("6. Split those minutes by the register's workstation: %s %s leads with %s, so delivery begins there, per terms "
      "of reference 2.5." % (F["start_ws"], F["start_ws_name"], c(F["b_by_ws"][F["start_ws"]])))
    a("7. Rebuilt each workstation's shifts from both roster workbooks and roster_changes_2025-26_2026-27.csv, took "
      "each shift's signaller as the one whose actions roc_signaller_actions_20251001_20260930.csv shows on that "
      "workstation (which also places every relief duty and the changes made on the day that the changes list "
      "lacks), counted hours on the clock across both clock changes, and split each signaller's hours at the "
      "second anniversary of the date qualified in signaller_competence_register.xlsx.")
    a("8. Read server B's stamps in ars_status_log_20251001_20260930.csv as Central European time (its copies of "
      "server A's events sit one hour behind in winter and two in summer), merged both servers into one event per "
      "change, mapped the old sub-area codes through the layout export, applied each workstation-wide switch-off "
      "to all of that workstation's sub-areas, and summed each sub-area's hours off within each UK calendar "
      "quarter.")
    a("")
    a("## 4. Deliverable Answers")
    a("")
    a("### improvement_plan_case_2027.pptx")
    a("")
    a("1. Programme B, the workstation display renewal, %s delay minutes." % c(F["call_minutes"]))
    a("2. Bar chart of those minutes by workstation, marking %s %s, where delivery begins:" % (
        F["start_ws"], F["start_ws_name"]))
    for w in ws_order:
        a("   - %s %s: %s" % (w, DESK[w], c(F["b_by_ws"][w])))
    a("")
    a("### staffing_and_ars_2025-26.xlsx")
    a("")
    a("3. Hours worked by workstation, by signallers then in their first two years since qualifying and by everyone "
      "else:")
    for w in DESK:
        a("   - %s %s: %s and %s" % (w, DESK[w], h(F["hours"][w]["first two years"]), h(F["hours"][w]["other"])))
    a("4. Sub-area hours with automatic route setting switched off, in total for each workstation, October to "
      "December 2025, January to March, April to June and July to September 2026:")
    for w in DESK:
        q = F["ars"][w]
        a("   - %s %s: %s, %s, %s and %s" % (w, DESK[w], h(q["2025 Q4"]), h(q["2026 Q1"]), h(q["2026 Q2"]),
                                           h(q["2026 Q3"])))
    a("")
    text = "\n".join(lines)
    assert "\u2014" not in text and "\u2013" not in text
    open(os.path.join(TASK, "submission.md"), "w", encoding="utf-8").write(text)


if __name__ == "__main__":
    main()
