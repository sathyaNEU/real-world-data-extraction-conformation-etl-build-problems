"""submission.md, written from figures.json (every figure emitted, none typed)."""
import common as C

QUARTERS = ["2025 Q4", "2026 Q1", "2026 Q2", "2026 Q3"]
MONTHS = ["2026-%02d" % m for m in range(1, 11)]
MNAME = dict(zip(MONTHS, ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                          "October"]))


def _and(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def label(code):
    return code + " (with XB-HRJ2)" if code in C.REPLACEMENT else code


def write(path, fig):
    tun, stay, traps = fig["call"]["tuning"], fig["call"]["stay"], fig["traps"]
    c = fig["counts"]
    L = []
    L += ["## Tags", "",
          "> **Domain:** Banking, credit and financial risk, fraud and AML detection.",
          "> **Analytical objective:** Anomaly detection and diagnostics.", ""]
    L += ["## 1. Final Recommendation", "",
          "**Put %s into the 2027 tuning, and no other scenario.**" % _and(tun),
          "Each is below the 3 per cent productivity floor over the twelve months to 30 September 2026 with every "
          "alert counted by how it will end. Not %s: their SARs so far are under 3 per cent of their decided alerts, but "
          "their investigations run longest, and the alerts still open on 2 November are mostly SARs to come." % _and(traps),
          ""]
    L += ["## 2. Critical Components", "",
          "1. Read over the alerts already decided, %s fall below the floor as well as %s." % (_and(traps), _and(tun)),
          "2. On 2 November %s had %s alerts from the year still under investigation." % (
              _and(traps), _and("{:,}".format(c[t]["undecided_in_investigation"]) for t in traps)),
          "3. In those scenarios an alert ending in a SAR is decided months after it is raised, while one closed without "
          "a SAR is closed within weeks, so an alert still undecided is far more likely than the scenario's average to "
          "end in a SAR.",
          "4. Counted by how they will end, %s clear the floor and %s stay below it." % (_and(traps), _and(tun)), ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Dated each alert in tm_alerts_2025-07_2026-10.csv by the business date of its run in "
          "tm_monitoring_runs_2025-07_2026-10.csv, left out the copies closed as duplicates and read XB-HRJ2 with XB-HRJ.",
          "2. Carried each escalated alert to its investigation in fcm_cases_export_2026-11-02.json: it ends in a SAR when "
          "the investigation's disposition is SAR filed; an alert still in triage or in an open investigation is undecided.",
          "3. For each scenario, read its alerts raised at least 330 days before the extract whose outcome is in: "
          "those that ended in a SAR were decided months after the alert, those that did not within weeks.",
          "4. Counted each undecided alert at the share of those older alerts of its scenario, still undecided at the "
          "same age, that ended in a SAR, and divided the SARs and expected SARs by the scenario's alerts in the year.",
          "5. Sent the scenarios below 3 per cent to the 2027 tuning.",
          "6. Investigations by quarter: each investigation in the export opened from 1 October 2025 to 30 September 2026 "
          "(Eastern date), counted once for the scenario of the alert whose escalation opened it (the alert whose triage "
          "closed at the investigation's opening).",
          "7. SARs by month: each filing in sar_filings_2025-07_2026-10.csv by its Eastern filing date, read along its "
          "investigation's filings in date order: the first is the initial report, a later one covering activity after "
          "the previous report is a continuing activity report whether or not its prior report field is filled, and one "
          "covering the same activity as the report it cites is a correction, left out.",
          "8. Recommended %s for the 2027 tuning." % _and(tun), ""]
    L += ["## 4. Deliverable Answers", "", "### tuning_scenarios_2027.docx", "",
          "1. Scenarios going into the 2027 tuning: %s." % _and(tun),
          "2. Scenarios staying out: %s." % _and(label(s) for s in stay),
          "3. Chart: each scenario's estimated productivity against the 3 per cent floor, %s in red, the only bars under "
          "the line." % _and(tun), "", "### tm_alert_figures_2026.xlsx", "",
          "4. Investigations each scenario's alerts opened, by quarter, whole numbers:"]
    for code in C.CODES:
        v = fig["ask_investigations"][code]
        L.append("   - %s: %s" % (label(code), ", ".join("%s %d" % (q, v[q]) for q in QUARTERS)))
    L.append("5. SARs filed in 2026 by month, initial and continuing activity, whole numbers:")
    for m in MONTHS:
        v = fig["ask_sars"][m]
        L.append("   - %s: initial %d, continuing activity %d" % (MNAME[m], v["initial"], v["continuing"]))
    L.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
