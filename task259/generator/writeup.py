"""submission.md and figures.json, every figure emitted from the analysis of target/."""
import json

from analysis import AREAS


def fmt_list(xs):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def build(F, M):
    names = F["names"]
    cert = [a for a in AREAS if a in F["certified"]]
    notc = [a for a in AREAS if a not in F["certified"]]
    par = M["par"]
    sh = F["share"]
    s_pct = round(100 * F["sensitivity"])
    raw_pct = round(100 * float(par["s_raw"]), 1)
    keep_pct = round(100 * float(par["s_raw"]) / F["sensitivity"])
    fp_pct = round(100 * F["false_report"], 1)
    r3 = M["rungs"]["R3_carry_face"]
    r3_set = [a for a in AREAS if r3[a] >= 7.0]
    figs = {
        "certified": [names[a] for a in cert],
        "not_certified": [names[a] for a in notc],
        "statewide_pct": round(F["statewide"]),
        "statewide_as_collected_pct": round(F["statewide_face"], 1),
        "sensitivity_pct": s_pct,
        "sensitivity_raw_pct": raw_pct,
        "persistence_pct": keep_pct,
        "false_report_pct": fp_pct,
        "shares_pct": {names[a]: round(sh[a], 1) for a in AREAS},
        "response_rate_pct": {names[a]: round(F["rr"][a], 1) for a in AREAS},
        "noncontact_rate_pct": {names[a]: round(F["nc"][a], 1) for a in AREAS},
        "threshold_pct": 7.0,
        "carry_rung_certified": [names[a] for a in r3_set],
        "codes": ["24.30.104", "59041", "LFSTAT 1 or 2", 0, 1, 2026, 216, 3],
    }
    cert_names = fmt_list([names[a] for a in cert])
    hi = ", ".join("%s %.1f" % (names[a], sh[a]) for a in cert)
    lo = ", ".join("%s %.1f" % (names[a], sh[a]) for a in notc)
    lines = []
    w = lines.append
    w("## Tags")
    w("")
    w("**Domain:** Survey Research & Official Statistics (nonresponse, calibration and measurement-error adjustment: "
      "a state household survey's multiple-jobholding rate by workforce area, on the respondent's own reporting basis "
      "when another household member answers for adults who are out at the interview).")
    w("**Analytical objective:** Descriptive & Distribution Analysis.")
    w("")
    w("## 1. Final Recommendation")
    w("")
    w("**Certify %s for the 2027 portable benefits pilot; %s do not qualify.** Counted as residents would report "
      "it themselves, %d%% of the state's employed residents held more than one job over 2025Q4 to 2026Q3, against "
      "%.1f%% as collected. Not the as-collected shares, the self-answered shares or shares imputed from "
      "self-answering residents alike in age, sex, hours and occupation, which all leave Silver Creek alone at 7.0%% "
      "or more: the residents answered for hold second jobs more often, and the answers given for them carry only "
      "%d%% of the second jobs those same residents report in the quarters they answer for themselves. Not carrying "
      "each resident's own answer from another quarter, which adds %s but leaves Northern Basin and Eastern Prairie "
      "below 7.0%% because about half of the answered-for residents never answer for themselves."
      % (cert_names, fmt_list([names[a] for a in notc]), round(F["statewide"]), F["statewide_face"], s_pct,
         fmt_list([names[a] for a in r3_set if a != "03"]) if len(r3_set) > 1 else "nothing"))
    w("")
    w("## 2. Critical Components")
    w("")
    w("1. Answered-for reports carry **%d%%** of the second jobs the same adults report themselves: in adjacent "
      "quarters where an employed adult answered for themselves in one and was answered for in the other (either "
      "order), the answered-for report carries the self-reported second job %.1f%% of the time, divided by the %d%% "
      "of self-reported second jobs still self-reported in the adjacent quarter." % (s_pct, raw_pct, keep_pct))
    w("2. Shares of employed residents holding more than one job on the residents' own reporting basis: %s "
      "(qualifying); %s." % (hi, lo))
    w("3. Statewide share on the same basis **%d%%** (as collected %.1f%%)." % (round(F["statewide"]),
                                                                                 F["statewide_face"]))
    w("")
    w("## 3. Step-by-Step Solution")
    w("")
    w("1. Kept employed residents (LFSTAT 1 or 2) in HES_PERSON_2025Q1_2026Q3.csv for 2025Q4 to 2026Q3 and joined "
      "each to its FWGT in HES_FINAL_WEIGHTS_2025Q4_2026Q3.xlsx by quarter, CASEID and LINENO, using the 2026Q3 rev "
      "sheet that HES_TECHNICAL_NOTE_2026-09.pdf says replaces the first issue; a record is the resident's own "
      "answer when RESPLINE equals LINENO.")
    w("2. Followed each adult across quarters by case and line number, carrying the CAPI 2026 case numbers back "
      "through HES_CASEID_CROSSWALK_CAPI2026.csv and breaking the chain where sex changes or age moves by other "
      "than 0 or 1 (a new household reuses line numbers).")
    w("3. Among adults employed in two adjacent quarters who answered for themselves in one and were answered for "
      "in the other (either order), the answered-for report carried the second job the adult reported themselves "
      "%.1f%% of the time; dividing by the %d%% of self-reported second jobs still self-reported in the adjacent "
      "quarter gives %d%%, and second jobs reported for adults who report none themselves, net of new second jobs, "
      "run at %.1f%%." % (raw_pct, keep_pct, s_pct, fp_pct))
    w("4. In each area, corrected the weighted share of answered-for residents reported with a second job as "
      "(reported share minus %.1f%%) divided by (%d%% minus %.1f%%), kept every self-answered record as given and "
      "combined both on the final weights: %s; %s." % (fp_pct, s_pct, fp_pct, hi, lo))
    w("5. Applied the same correction statewide: %d%% against %.1f%% as collected." % (round(F["statewide"]),
                                                                                      F["statewide_face"]))
    w("6. For the survey quality sheet, counted each housing unit once per quarter by FRAMEID in "
      "HES_HOUSEHOLD_DISPOSITIONS_2025Q1_2026Q3.csv (an interview code in any of its rows makes it interviewed, "
      "which covers converted refusals and the old system's second record of some 2026Q2 interviews), placed it by "
      "CTY with county 59041 split by ZIP (TDLI_WORKFORCE_AREAS_2026.xlsx), and took as not eligible the units "
      "coded vacant, demolished or not a housing unit plus, per the response-rate definitions in "
      "HES_TECHNICAL_NOTE_2026-09.pdf, the units the master address file as finally corrected shows removed as "
      "vacant or demolished on or before the visit date, replaying HES_FRAME_MAINTENANCE_2024-07_2026-09.csv in "
      "date order with each RESTORE (DELETED IN ERROR) cancelling the removal it follows from that removal's date; "
      "response rate is interviewed over eligible, noncontact rate is eligible units coded no one home (3 or 216) "
      "over eligible.")
    w("7. Recommended certifying %s, the areas at or above 7.0%%." % cert_names)
    w("")
    w("## 4. Deliverable Answers")
    w("")
    w("### pba_pilot_areas_2027.xlsx")
    w("")
    w("1. Qualify for the 2027 pilot: %s." % cert_names)
    w("2. Do not qualify: %s." % fmt_list([names[a] for a in notc]))
    w("3. Statewide share of employed residents holding more than one job on the rule's basis: %d%%."
      % round(F["statewide"]))
    w("4. Household response rate by workforce area, 2025Q4 to 2026Q3, percent to one decimal:")
    for a in AREAS:
        w("   - %s: %.1f" % (names[a], F["rr"][a]))
    w("5. Noncontact rate by workforce area, 2025Q4 to 2026Q3, percent to one decimal:")
    for a in AREAS:
        w("   - %s: %.1f" % (names[a], F["nc"][a]))
    w("")
    w("### pba_pilot_certification_2027.docx")
    w("")
    w("6. Memo to the commissioner recommending %s, with a bar chart of every area's share against the 7 percent "
      "line on page 1, qualifying areas in dark bars." % cert_names)
    w("")
    return "\n".join(lines), figs


def write(F, M, sub_path, fig_path):
    text, figs = build(F, M)
    with open(sub_path, "w", encoding="utf-8") as f:
        f.write(text)
    with open(fig_path, "w", encoding="utf-8") as f:
        json.dump(figs, f, indent=1, sort_keys=True)
        f.write("\n")
